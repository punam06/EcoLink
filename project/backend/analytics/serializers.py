from rest_framework import serializers
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from files.models import FileAsset


class AnalyticsSummarySerializer(serializers.Serializer):
    """Serializer for analytics summary data"""
    
    total_files = serializers.IntegerField()
    total_size_bytes = serializers.IntegerField()
    total_size_gb = serializers.FloatField()
    total_co2_saved_g = serializers.FloatField()
    total_kwh_saved = serializers.FloatField()
    duplicates_count = serializers.IntegerField()
    duplicates_percentage = serializers.FloatField()
    average_impact_score = serializers.FloatField()
    files_this_month = serializers.IntegerField()
    co2_saved_this_month = serializers.FloatField()


class FileTypeAnalyticsSerializer(serializers.Serializer):
    """Serializer for file type analytics"""
    
    mime_type = serializers.CharField()
    count = serializers.IntegerField()
    total_size_bytes = serializers.IntegerField()
    average_impact_score = serializers.FloatField()


class ImpactTrendSerializer(serializers.Serializer):
    """Serializer for impact trend data"""
    
    date = serializers.DateField()
    files_count = serializers.IntegerField()
    total_co2_g = serializers.FloatField()
    total_kwh = serializers.FloatField()
    duplicates_count = serializers.IntegerField()