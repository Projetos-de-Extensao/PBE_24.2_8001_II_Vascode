from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductFeedbackViewSet

router = DefaultRouter()
router.register(r'product-feedback', ProductFeedbackViewSet, basename='product-feedback')

urlpatterns = [
    path('', include(router.urls)),
]
