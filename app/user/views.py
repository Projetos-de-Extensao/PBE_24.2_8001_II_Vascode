from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User  # Seu modelo de usuário customizado
from .serializers import UserCreateSerializer, UserUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import make_password  # Para criptografar a senha

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    # Registro de novos usuários
    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        responses={201: UserCreateSerializer, 400: 'Bad Request'}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='register')
    def register(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = User(
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
                password=make_password(serializer.validated_data['password'])  # Criptografa a senha
            )
            user.save()
            response_data = serializer.data
            response_data['id'] = user.id  # Incluindo o ID do usuário na resposta
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Atualização de informações do usuário
    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserUpdateSerializer, 400: 'Bad Request', 403: 'Forbidden', 404: 'Not Found'}
    )
    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated], url_path='update')
    def update_user(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({"error": "Você não tem permissão para atualizar este usuário."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in serializer.validated_data:
                user.password = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
