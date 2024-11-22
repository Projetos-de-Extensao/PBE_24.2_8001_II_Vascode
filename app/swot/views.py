from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SWOTAnalysis
from .serializers import (
    SWOTAnalysisSerializer,
    SWOTAnalysisCreateSerializer,
    SWOTAnalysisDetailSerializer,
    SWOTAnalysisUpdateSerializer
)
from django.utils import timezone
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema


class SWOTAnalysisViewSet(viewsets.ModelViewSet):
    queryset = SWOTAnalysis.objects.all()
    serializer_class = SWOTAnalysisSerializer

    # Criar nova análise SWOT
    @swagger_auto_schema(request_body=SWOTAnalysisCreateSerializer)
    def create(self, request, *args, **kwargs):
        serializer = SWOTAnalysisCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Extraindo o user_id para criar a instância de SWOTAnalysis
            user_id = serializer.validated_data['user_id'].id if hasattr(serializer.validated_data['user_id'], 'id') else serializer.validated_data['user_id']
            swot_analysis = SWOTAnalysis.objects.create(
                user_id=user_id,
                strengths=serializer.validated_data['strengths'],
                weaknesses=serializer.validated_data['weaknesses'],
                opportunities=serializer.validated_data['opportunities'],
                threats=serializer.validated_data['threats']
            )
            response_serializer = SWOTAnalysisSerializer(swot_analysis)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Atualizar uma análise SWOT
    @swagger_auto_schema(request_body=SWOTAnalysisUpdateSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # Salvar análise parcial
    @swagger_auto_schema(request_body=SWOTAnalysisUpdateSerializer)
    @action(detail=True, methods=['patch'], url_path='save-partial')
    def save_partial(self, request, pk=None):
        try:
            swot = SWOTAnalysis.objects.get(pk=pk, user_id=request.user.id)
            serializer = SWOTAnalysisUpdateSerializer(swot, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SWOTAnalysis.DoesNotExist:
            return Response({'error': 'Análise SWOT não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # Periodicidade da Análise para um usuário específico
    @action(detail=True, methods=['get'], url_path='check-periodicity')
    def check_periodicity(self, request, pk=None):
        last_analysis = SWOTAnalysis.objects.filter(user_id=pk).order_by('-created_at').first()
        if last_analysis and (timezone.now() - last_analysis.created_at) < timedelta(days=30):
            return Response({'error': 'Ainda não está permitido criar nova análise SWOT.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Você pode criar uma nova análise SWOT.'}, status=status.HTTP_200_OK)

    # Histórico de análises anteriores de um usuário específico
    @swagger_auto_schema(responses={200: SWOTAnalysisDetailSerializer(many=True)})
    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        analyses = SWOTAnalysis.objects.filter(user_id=pk).order_by('-created_at')
        serializer = SWOTAnalysisDetailSerializer(analyses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
