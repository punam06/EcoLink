import hashlib
import magic
import structlog
from io import BytesIO
from celery import shared_task
from django.contrib.auth.models import User
from django.conf import settings
from boto3 import client
from botocore.exceptions import ClientError

from .models import FileAsset, Recommendation

logger = structlog.get_logger(__name__)


@shared_task
def analyze_file(user_id, bucket, key, filename, size_bytes):
    """
    Analyze an uploaded file for environmental impact and generate recommendations.
    
    Args:
        user_id: ID of the user who uploaded the file
        bucket: S3 bucket name
        key: S3 object key
        filename: Original filename
        size_bytes: File size in bytes
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"Starting file analysis for {filename} by user {user.username}")
        
        # Initialize S3 client
        s3_client = client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            use_ssl=settings.AWS_S3_USE_SSL
        )
        
        # Download file from S3 and compute SHA-256
        file_buffer = BytesIO()
        s3_client.download_fileobj(bucket, key, file_buffer)
        file_buffer.seek(0)
        
        # Compute SHA-256 hash
        sha256_hash = hashlib.sha256()
        file_content = file_buffer.read()
        sha256_hash.update(file_content)
        file_sha256 = sha256_hash.hexdigest()
        
        # Detect MIME type
        mime_type = magic.from_buffer(file_content, mime=True)
        
        # Check for duplicates
        duplicate_file = FileAsset.objects.filter(sha256=file_sha256).exclude(user=user).first()
        
        # Calculate environmental impact
        size_gb = size_bytes / (1024 * 1024 * 1024)
        kwh_estimate = size_gb * settings.REGION_KWH_PER_GB
        co2_g_estimate = kwh_estimate * settings.REGION_CO2_G_PER_KWH
        
        # Calculate impact score (0-100)
        impact_score = min(100, int((size_gb * 100) + (co2_g_estimate / 1000 * 10)))
        
        # Create storage URL
        storage_url = f"{settings.AWS_S3_ENDPOINT_URL}/{bucket}/{key}"
        
        # Create FileAsset record
        file_asset = FileAsset.objects.create(
            user=user,
            filename=filename,
            size_bytes=size_bytes,
            mime_type=mime_type,
            sha256=file_sha256,
            storage_url=storage_url,
            duplicate_of=duplicate_file,
            kwh_estimate=kwh_estimate,
            co2_g_estimate=co2_g_estimate,
            impact_score=impact_score
        )
        
        # Generate recommendations
        recommendations = _generate_recommendations(file_asset)
        
        # Create recommendation records
        for rec in recommendations:
            Recommendation.objects.create(
                file=file_asset,
                kind=rec['kind'],
                message=rec['message']
            )
        
        logger.info(f"File analysis completed for {filename}. Impact score: {impact_score}")
        
        return {
            'file_id': file_asset.id,
            'sha256': file_sha256,
            'mime_type': mime_type,
            'is_duplicate': bool(duplicate_file),
            'impact_score': impact_score,
            'recommendations_count': len(recommendations)
        }
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        raise
    except ClientError as e:
        logger.error(f"S3 error while analyzing file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during file analysis: {e}")
        raise


def _generate_recommendations(file_asset):
    """Generate recommendations based on file characteristics"""
    recommendations = []
    
    # Duplicate recommendation
    if file_asset.duplicate_of:
        recommendations.append({
            'kind': 'duplicate',
            'message': f'This file is identical to "{file_asset.duplicate_of.filename}". '
                      f'Consider reusing the existing file to save {file_asset.co2_g_estimate:.1f}g CO2.'
        })
    
    # Large file compression recommendation
    if file_asset.size_mb > 10:  # Files larger than 10MB
        recommendations.append({
            'kind': 'compress',
            'message': f'This {file_asset.size_mb:.1f}MB file could potentially be compressed '
                      f'to reduce storage and transfer energy consumption.'
        })
    
    # Video/media sharing recommendation
    if file_asset.mime_type and any(t in file_asset.mime_type for t in ['video', 'audio']):
        if file_asset.size_mb > 50:
            recommendations.append({
                'kind': 'share_link',
                'message': 'For large media files, consider sharing a streaming link instead '
                          'of distributing the file directly to reduce bandwidth usage.'
            })
    
    # Archive recommendation for old duplicates
    if file_asset.size_mb > 100:  # Large files
        recommendations.append({
            'kind': 'optimize',
            'message': f'This large file ({file_asset.size_mb:.1f}MB) has a high environmental '
                      f'impact ({file_asset.co2_g_estimate:.1f}g CO2). Consider optimizing '
                      f'or archiving if not frequently accessed.'
        })
    
    return recommendations