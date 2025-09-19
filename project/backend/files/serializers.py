from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FileAsset, Recommendation


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Recommendation model"""
    
    kind_display = serializers.CharField(source='get_kind_display', read_only=True)
    
    class Meta:
        model = Recommendation
        fields = ['id', 'kind', 'kind_display', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class FileAssetSerializer(serializers.ModelSerializer):
    """Serializer for FileAsset model"""
    
    user = UserSerializer(read_only=True)
    duplicate_of = serializers.SerializerMethodField()
    recommendations = RecommendationSerializer(many=True, read_only=True)
    is_duplicate = serializers.ReadOnlyField()
    size_mb = serializers.ReadOnlyField()
    size_gb = serializers.ReadOnlyField()
    
    class Meta:
        model = FileAsset
        fields = [
            'id', 'user', 'filename', 'size_bytes', 'size_mb', 'size_gb',
            'mime_type', 'sha256', 'storage_url', 'duplicate_of', 'is_duplicate',
            'kwh_estimate', 'co2_g_estimate', 'impact_score',
            'recommendations', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'sha256', 'storage_url', 'duplicate_of',
            'kwh_estimate', 'co2_g_estimate', 'impact_score',
            'created_at', 'updated_at'
        ]
    
    def get_duplicate_of(self, obj):
        """Return basic info about the duplicate file if it exists"""
        if obj.duplicate_of:
            return {
                'id': obj.duplicate_of.id,
                'filename': obj.duplicate_of.filename,
                'user': obj.duplicate_of.user.username,
                'created_at': obj.duplicate_of.created_at
            }
        return None


class FileAssetListSerializer(serializers.ModelSerializer):
    """Simplified serializer for file listing"""
    
    user = serializers.CharField(source='user.username', read_only=True)
    is_duplicate = serializers.ReadOnlyField()
    size_mb = serializers.ReadOnlyField()
    recommendations_count = serializers.SerializerMethodField()
    
    class Meta:
        model = FileAsset
        fields = [
            'id', 'user', 'filename', 'size_bytes', 'size_mb',
            'mime_type', 'is_duplicate', 'impact_score',
            'recommendations_count', 'created_at'
        ]
    
    def get_recommendations_count(self, obj):
        return obj.recommendations.count()


class FileCommitSerializer(serializers.Serializer):
    """Serializer for committing a file upload"""
    
    bucket = serializers.CharField(max_length=255)
    key = serializers.CharField(max_length=500)
    filename = serializers.CharField(max_length=255)
    size_bytes = serializers.IntegerField(min_value=1)
    
    def validate_size_bytes(self, value):
        """Validate file size against maximum allowed"""
        from django.conf import settings
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 500 * 1024 * 1024)
        if value > max_size:
            raise serializers.ValidationError(f'File size exceeds maximum allowed size of {max_size} bytes')
        return value