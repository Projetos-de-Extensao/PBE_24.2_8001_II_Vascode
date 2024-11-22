from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet

router = DefaultRouter()
router.register(r'member', MemberViewSet, basename='member')

urlpatterns = [
    path('', include(router.urls)),
]
