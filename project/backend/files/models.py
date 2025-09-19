from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class FileAsset(models.Model):
    """Model representing a file uploaded to the system"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    filename = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField(validators=[MinValueValidator(0)])
    mime_type = models.CharField(max_length=255, blank=True, null=True)
    sha256 = models.CharField(max_length=64, db_index=True)  # SHA-256 hash for duplicate detection
    storage_url = models.URLField(max_length=500, blank=True, null=True)  # S3 URL
    duplicate_of = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='duplicates'
    )
    
    # Environmental impact estimates
    kwh_estimate = models.FloatField(
        validators=[MinValueValidator(0.0)], 
        help_text="Estimated kWh energy consumption"
    )
    co2_g_estimate = models.FloatField(
        validators=[MinValueValidator(0.0)], 
        help_text="Estimated CO2 emissions in grams"
    )
    impact_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Impact score from 0-100"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'files_fileasset'
        indexes = [
            models.Index(fields=['sha256']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.filename} ({self.user.username})"
    
    @property
    def is_duplicate(self):
        """Check if this file is a duplicate of another"""
        return self.duplicate_of is not None
    
    @property
    def size_mb(self):
        """Return file size in MB"""
        return self.size_bytes / (1024 * 1024)
    
    @property
    def size_gb(self):
        """Return file size in GB"""
        return self.size_bytes / (1024 * 1024 * 1024)


class Recommendation(models.Model):
    """Model for storing recommendations for files"""
    
    RECOMMENDATION_KINDS = [
        ('duplicate', 'Reuse Existing File'),
        ('compress', 'Compress File'),
        ('share_link', 'Share Link Instead'),
        ('archive', 'Archive Old File'),
        ('optimize', 'Optimize File'),
    ]
    
    file = models.ForeignKey(FileAsset, on_delete=models.CASCADE, related_name='recommendations')
    kind = models.CharField(max_length=20, choices=RECOMMENDATION_KINDS)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'files_recommendation'
        indexes = [
            models.Index(fields=['file', '-created_at']),
            models.Index(fields=['kind']),
        ]
    
    def __str__(self):
        return f"{self.get_kind_display()} for {self.file.filename}"
