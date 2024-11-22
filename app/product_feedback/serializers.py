from rest_framework import serializers
from .models import ProductFeedback

class ProductFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeedback
        fields = ['id', 'user', 'user_id', 'feedback_text', 'feedback_type', 'created_at']
        read_only_fields = ['user', 'created_at']

class ProductFeedbackCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProductFeedback
        fields = ['user_id', 'feedback_text', 'feedback_type']

class ProductFeedbackDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductFeedback
        fields = ['id', 'user', 'user_id', 'feedback_text', 'feedback_type', 'created_at']
        read_only_fields = ['user_id']

class ProductFeedbackUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = ProductFeedback
        fields = ['user_id', 'feedback_text', 'feedback_type']
