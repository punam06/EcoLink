from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileAssetViewSet, RecommendationViewSet

router = DefaultRouter()
router.register(r'files', FileAssetViewSet, basename='file')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
]