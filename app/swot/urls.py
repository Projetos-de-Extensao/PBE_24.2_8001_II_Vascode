from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SWOTAnalysisViewSet

router = DefaultRouter()
router.register(r'swot', SWOTAnalysisViewSet, basename='swot')

urlpatterns = [
    path('', include(router.urls)),
]