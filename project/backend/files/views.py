import uuid
from datetime import datetime, timedelta
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from boto3 import client
from botocore.exceptions import ClientError
import structlog

from .models import FileAsset, Recommendation
from .serializers import (
    FileAssetSerializer, FileAssetListSerializer, 
    RecommendationSerializer, FileCommitSerializer
)
from .tasks import analyze_file

logger = structlog.get_logger(__name__)


class FileAssetViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for FileAsset operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FileAssetListSerializer
        return FileAssetSerializer
    
    def get_queryset(self):
        """Return files for the current user"""
        return FileAsset.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=False, methods=['post'], url_path='request-upload-url')
    def request_upload_url(self, request):
        """Generate a presigned URL for file upload to S3"""
        try:
            filename = request.data.get('filename')
            content_type = request.data.get('content_type', 'application/octet-stream')
            
            if not filename:
                return Response(
                    {'error': 'filename is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generate unique key for S3
            file_key = f"uploads/{request.user.id}/{uuid.uuid4().hex}_{filename}"
            
            # Initialize S3 client
            s3_client = client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
                use_ssl=settings.AWS_S3_USE_SSL
            )
            
            # Generate presigned URL for PUT operation
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': file_key,
                    'ContentType': content_type,
                },
                ExpiresIn=3600,  # 1 hour
                HttpMethod='PUT'
            )
            
            logger.info(f"Generated presigned URL for {filename} by user {request.user.username}")
            
            return Response({
                'upload_url': presigned_url,
                'bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'key': file_key,
                'expires_in': 3600
            })
            
        except ClientError as e:
            logger.error(f"S3 error generating presigned URL: {e}")
            return Response(
                {'error': 'Failed to generate upload URL'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error generating presigned URL: {e}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='commit')
    def commit_upload(self, request):
        """Commit a file upload and trigger analysis"""
        serializer = FileCommitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        try:
            # Trigger async analysis task
            task_result = analyze_file.delay(
                user_id=request.user.id,
                bucket=data['bucket'],
                key=data['key'],
                filename=data['filename'],
                size_bytes=data['size_bytes']
            )
            
            logger.info(f"Queued analysis task {task_result.id} for {data['filename']}")
            
            return Response({
                'message': 'File upload committed successfully',
                'task_id': task_result.id,
                'filename': data['filename'],
                'size_bytes': data['size_bytes']
            }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            logger.error(f"Error committing file upload: {e}")
            return Response(
                {'error': 'Failed to process file upload'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='download-url')
    def get_download_url(self, request, pk=None):
        """Generate a presigned URL for file download"""
        try:
            file_asset = self.get_object()
            
            # Extract key from storage_url
            storage_url = file_asset.storage_url
            if not storage_url:
                return Response(
                    {'error': 'File storage URL not available'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Parse the key from the storage URL
            key = storage_url.split('/')[-1]  # Simple extraction, could be improved
            
            # Initialize S3 client
            s3_client = client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
                use_ssl=settings.AWS_S3_USE_SSL
            )
            
            # Generate presigned URL for GET operation
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': key,
                },
                ExpiresIn=3600,  # 1 hour
                HttpMethod='GET'
            )
            
            return Response({
                'download_url': presigned_url,
                'expires_in': 3600,
                'filename': file_asset.filename
            })
            
        except ClientError as e:
            logger.error(f"S3 error generating download URL: {e}")
            return Response(
                {'error': 'Failed to generate download URL'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error generating download URL: {e}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Recommendation operations"""
    
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return recommendations for the current user's files"""
        return Recommendation.objects.filter(
            file__user=self.request.user
        ).select_related('file').order_by('-created_at')
