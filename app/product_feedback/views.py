from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ProductFeedback
from .serializers import (
    ProductFeedbackSerializer,
    ProductFeedbackCreateSerializer,
    ProductFeedbackDetailSerializer,
    ProductFeedbackUpdateSerializer,
)

class ProductFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ProductFeedback.objects.all()

    def get_serializer_class(self):
        """Define qual serializer usar dependendo da ação."""
        if self.action == 'create':
            return ProductFeedbackCreateSerializer
        elif self.action == 'retrieve':
            return ProductFeedbackDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductFeedbackUpdateSerializer
        return ProductFeedbackSerializer

    def perform_create(self, serializer):
        """Define o comportamento ao criar um novo feedback."""
        user_id = self.request.data.get('user_id')
        serializer.save(user_id=user_id)

    @action(detail=False, methods=['post'], url_path='send-partial-feedback')
    def send_partial_feedback(self, request):
        """Método customizado para enviar feedback parcial."""
        serializer = ProductFeedbackCreateSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id')
            serializer.save(user_id=user_id)
            return Response({'message': 'Feedback enviado com sucesso.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='confirm-submission')
    def confirm_submission(self, request, pk=None):
        """Confirmação do envio do feedback, checando se existe."""
        try:
            feedback = ProductFeedback.objects.get(pk=pk)
            return Response({'status': 'Feedback encontrado. Envio confirmado.'}, status=status.HTTP_200_OK)
        except ProductFeedback.DoesNotExist:
            return Response({'error': 'Feedback não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'], url_path='update-feedback')
    def update_feedback(self, request, pk=None):
        """Método customizado para atualizar um feedback."""
        try:
            feedback = ProductFeedback.objects.get(pk=pk)
        except ProductFeedback.DoesNotExist:
            return Response({'error': 'Feedback não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductFeedbackUpdateSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Feedback atualizado com sucesso.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete-feedback')
    def delete_feedback(self, request, pk=None):
        """Método customizado para deletar um feedback."""
        try:
            feedback = ProductFeedback.objects.get(pk=pk)
        except ProductFeedback.DoesNotExist:
            return Response({'error': 'Feedback não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        feedback.delete()
        return Response({'message': 'Feedback deletado com sucesso.'}, status=status.HTTP_200_OK)