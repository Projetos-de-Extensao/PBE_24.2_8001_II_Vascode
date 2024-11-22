from app.user.models import User
from rest_framework import serializers
from .models import SWOTAnalysis

class SWOTAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTAnalysis
        fields = ['id', 'user_id', 'strengths', 'weaknesses', 'opportunities', 'threats', 'created_at']
        read_only_fields = ['created_at']

class SWOTAnalysisCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SWOTAnalysis
        fields = ['user_id', 'strengths', 'weaknesses', 'opportunities', 'threats']

    def create(self, validated_data):
        user = validated_data.pop('user_id')
        return SWOTAnalysis.objects.create(user=user, **validated_data)

class SWOTAnalysisDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField()

    class Meta:
        model = SWOTAnalysis
        fields = ['id', 'user_id', 'strengths', 'weaknesses', 'opportunities', 'threats', 'created_at']

class SWOTAnalysisUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTAnalysis
        fields = ['strengths', 'weaknesses', 'opportunities', 'threats']