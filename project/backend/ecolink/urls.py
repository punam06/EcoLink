"""
URL configuration for ecolink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def health_check(request):
    """Simple health check endpoint for deployment monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'ecolink-backend',
        'version': '1.0.0'
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Health check
    path('api/health/', health_check, name='health_check'),
    
    # Authentication endpoints
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API v1 endpoints
    path('api/v1/', include('files.urls')),
    path('api/v1/', include('analytics.urls')),
]
