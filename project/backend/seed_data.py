#!/usr/bin/env python
"""
Django management script to create demo data for EcoLink.
Run with: python manage.py shell < seed_data.py
"""

import os
import django
from django.contrib.auth.models import User
from files.models import FileAsset, Recommendation

# Demo user credentials
DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo123"
DEMO_EMAIL = "demo@ecolink.com"

def create_demo_user():
    """Create or get the demo user"""
    user, created = User.objects.get_or_create(
        username=DEMO_USERNAME,
        defaults={
            'email': DEMO_EMAIL,
            'first_name': 'Demo',
            'last_name': 'User',
        }
    )
    
    if created:
        user.set_password(DEMO_PASSWORD)
        user.save()
        print(f"✅ Created demo user: {DEMO_USERNAME}")
    else:
        print(f"✅ Demo user already exists: {DEMO_USERNAME}")
    
    return user

def create_sample_files(user):
    """Create sample file records for demonstration"""
    
    # Sample file data
    sample_files = [
        {
            'filename': 'presentation.pdf',
            'size_bytes': 5242880,  # 5MB
            'mime_type': 'application/pdf',
            'sha256': 'a1b2c3d4e5f6789012345678901234567890abcdef',
            'storage_url': 'http://localhost:9000/ecolink/uploads/1/presentation.pdf',
            'kwh_estimate': 0.030,
            'co2_g_estimate': 12.0,
            'impact_score': 25,
        },
        {
            'filename': 'image.jpg',
            'size_bytes': 2097152,  # 2MB
            'mime_type': 'image/jpeg',
            'sha256': 'b2c3d4e5f6789012345678901234567890abcdef12',
            'storage_url': 'http://localhost:9000/ecolink/uploads/1/image.jpg',
            'kwh_estimate': 0.012,
            'co2_g_estimate': 4.8,
            'impact_score': 15,
        },
        {
            'filename': 'video.mp4',
            'size_bytes': 52428800,  # 50MB
            'mime_type': 'video/mp4',
            'sha256': 'c3d4e5f6789012345678901234567890abcdef123',
            'storage_url': 'http://localhost:9000/ecolink/uploads/1/video.mp4',
            'kwh_estimate': 0.300,
            'co2_g_estimate': 120.0,
            'impact_score': 75,
        },
        {
            'filename': 'presentation_copy.pdf',  # Duplicate
            'size_bytes': 5242880,  # 5MB
            'mime_type': 'application/pdf',
            'sha256': 'a1b2c3d4e5f6789012345678901234567890abcdef',  # Same hash as first
            'storage_url': 'http://localhost:9000/ecolink/uploads/1/presentation_copy.pdf',
            'kwh_estimate': 0.030,
            'co2_g_estimate': 12.0,
            'impact_score': 25,
        },
    ]
    
    created_files = []
    
    for file_data in sample_files:
        file_asset = FileAsset.objects.create(
            user=user,
            **file_data
        )
        created_files.append(file_asset)
        print(f"✅ Created sample file: {file_data['filename']}")
    
    # Set up duplicate relationship
    if len(created_files) >= 4:
        created_files[3].duplicate_of = created_files[0]  # presentation_copy is duplicate of presentation
        created_files[3].save()
        print(f"✅ Set duplicate relationship: {created_files[3].filename} -> {created_files[0].filename}")
    
    return created_files

def create_sample_recommendations(files):
    """Create sample recommendations for the files"""
    
    recommendations_data = [
        {
            'file': files[0],  # presentation.pdf
            'kind': 'compress',
            'message': 'This PDF file could be compressed to reduce its environmental impact by approximately 30%.',
        },
        {
            'file': files[2],  # video.mp4
            'kind': 'share_link',
            'message': 'Consider sharing this large video file via a streaming link instead of direct download to reduce bandwidth usage.',
        },
        {
            'file': files[3] if len(files) > 3 else files[0],  # presentation_copy.pdf (duplicate)
            'kind': 'duplicate',
            'message': 'This file is identical to "presentation.pdf". Reusing the existing file would save 12.0g of CO2.',
        },
    ]
    
    for rec_data in recommendations_data:
        recommendation = Recommendation.objects.create(**rec_data)
        print(f"✅ Created recommendation for {rec_data['file'].filename}: {rec_data['kind']}")

def main():
    """Main function to seed the database"""
    print("🌱 Seeding EcoLink database with demo data...")
    
    # Create demo user
    demo_user = create_demo_user()
    
    # Create sample files
    sample_files = create_sample_files(demo_user)
    
    # Create sample recommendations
    create_sample_recommendations(sample_files)
    
    print(f"\n✅ Database seeding complete!")
    print(f"📝 Demo login credentials:")
    print(f"   Username: {DEMO_USERNAME}")
    print(f"   Password: {DEMO_PASSWORD}")
    print(f"\n🚀 You can now start the application and log in with these credentials.")

if __name__ == "__main__":
    main()