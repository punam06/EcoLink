from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, date
import structlog

from files.models import FileAsset
from .serializers import (
    AnalyticsSummarySerializer, 
    FileTypeAnalyticsSerializer,
    ImpactTrendSerializer
)

logger = structlog.get_logger(__name__)


class AnalyticsViewSet(viewsets.GenericViewSet):
    """ViewSet for analytics operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='summary')
    def get_summary(self, request):
        """Get comprehensive analytics summary for the user"""
        try:
            user_files = FileAsset.objects.filter(user=request.user)
            
            # Basic metrics
            total_files = user_files.count()
            
            if total_files == 0:
                return Response({
                    'total_files': 0,
                    'total_size_bytes': 0,
                    'total_size_gb': 0.0,
                    'total_co2_saved_g': 0.0,
                    'total_kwh_saved': 0.0,
                    'duplicates_count': 0,
                    'duplicates_percentage': 0.0,
                    'average_impact_score': 0.0,
                    'files_this_month': 0,
                    'co2_saved_this_month': 0.0
                })
            
            # Aggregate data
            aggregates = user_files.aggregate(
                total_size=Sum('size_bytes'),
                total_co2=Sum('co2_g_estimate'),
                total_kwh=Sum('kwh_estimate'),
                avg_impact=Avg('impact_score')
            )
            
            # Calculate duplicates
            duplicates_count = user_files.filter(duplicate_of__isnull=False).count()
            duplicates_percentage = (duplicates_count / total_files) * 100 if total_files > 0 else 0
            
            # CO2 saved from duplicates (estimated)
            duplicate_files = user_files.filter(duplicate_of__isnull=False)
            total_co2_saved_g = duplicate_files.aggregate(saved=Sum('co2_g_estimate'))['saved'] or 0
            total_kwh_saved = duplicate_files.aggregate(saved=Sum('kwh_estimate'))['saved'] or 0
            
            # This month's data
            first_day_this_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            this_month_files = user_files.filter(created_at__gte=first_day_this_month)
            files_this_month = this_month_files.count()
            co2_saved_this_month = this_month_files.filter(
                duplicate_of__isnull=False
            ).aggregate(saved=Sum('co2_g_estimate'))['saved'] or 0
            
            summary_data = {
                'total_files': total_files,
                'total_size_bytes': aggregates['total_size'] or 0,
                'total_size_gb': round((aggregates['total_size'] or 0) / (1024**3), 2),
                'total_co2_saved_g': round(total_co2_saved_g, 2),
                'total_kwh_saved': round(total_kwh_saved, 4),
                'duplicates_count': duplicates_count,
                'duplicates_percentage': round(duplicates_percentage, 1),
                'average_impact_score': round(aggregates['avg_impact'] or 0, 1),
                'files_this_month': files_this_month,
                'co2_saved_this_month': round(co2_saved_this_month, 2)
            }
            
            serializer = AnalyticsSummarySerializer(summary_data)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting analytics summary: {e}")
            return Response({'error': 'Failed to fetch analytics summary'}, status=500)
    
    @action(detail=False, methods=['get'], url_path='file-types')
    def get_file_types(self, request):
        """Get analytics breakdown by file type"""
        try:
            user_files = FileAsset.objects.filter(user=request.user)
            
            # Group by MIME type
            file_type_data = user_files.values('mime_type').annotate(
                count=Count('id'),
                total_size_bytes=Sum('size_bytes'),
                average_impact_score=Avg('impact_score')
            ).order_by('-total_size_bytes')
            
            # Clean up None mime_types
            for item in file_type_data:
                if item['mime_type'] is None:
                    item['mime_type'] = 'Unknown'
                item['average_impact_score'] = round(item['average_impact_score'] or 0, 1)
            
            serializer = FileTypeAnalyticsSerializer(file_type_data, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting file type analytics: {e}")
            return Response({'error': 'Failed to fetch file type analytics'}, status=500)
    
    @action(detail=False, methods=['get'], url_path='impact-trend')
    def get_impact_trend(self, request):
        """Get daily impact trend for the last 30 days"""
        try:
            days = int(request.query_params.get('days', 30))
            start_date = timezone.now().date() - timedelta(days=days)
            
            user_files = FileAsset.objects.filter(
                user=request.user,
                created_at__date__gte=start_date
            )
            
            # Group by date
            trend_data = []
            current_date = start_date
            end_date = timezone.now().date()
            
            while current_date <= end_date:
                day_files = user_files.filter(created_at__date=current_date)
                day_aggregates = day_files.aggregate(
                    total_co2=Sum('co2_g_estimate'),
                    total_kwh=Sum('kwh_estimate')
                )
                
                trend_data.append({
                    'date': current_date,
                    'files_count': day_files.count(),
                    'total_co2_g': round(day_aggregates['total_co2'] or 0, 2),
                    'total_kwh': round(day_aggregates['total_kwh'] or 0, 4),
                    'duplicates_count': day_files.filter(duplicate_of__isnull=False).count()
                })
                
                current_date += timedelta(days=1)
            
            serializer = ImpactTrendSerializer(trend_data, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting impact trend: {e}")
            return Response({'error': 'Failed to fetch impact trend'}, status=500)
