from rest_framework import serializers
from .models import SWOTAnalysis

class SWOTAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTAnalysis
        fields = ['id', 'user', 'strengths', 'weaknesses', 'opportunities', 'threats', 'created_at']
        read_only_fields = ['user', 'created_at']

class SWOTAnalysisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTAnalysis
        fields = ['strengths', 'weaknesses', 'opportunities', 'threats']

class SWOTAnalysisDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = SWOTAnalysis
        fields = ['id', 'user', 'strengths', 'weaknesses', 'opportunities', 'threats', 'created_at']

class SWOTAnalysisUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTAnalysis
        fields = ['strengths', 'weaknesses', 'opportunities', 'threats']
