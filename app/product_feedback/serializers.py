from rest_framework import serializers
from .models import ProductFeedback

class ProductFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeedback
        fields = ['id', 'user', 'feedback_text', 'feedback_type', 'created_at']
        read_only_fields = ['user', 'created_at']

class ProductFeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeedback
        fields = ['feedback_text', 'feedback_type']

class ProductFeedbackDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductFeedback
        fields = ['id', 'user', 'feedback_text', 'feedback_type', 'created_at']

class ProductFeedbackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeedback
        fields = ['feedback_text', 'feedback_type']
