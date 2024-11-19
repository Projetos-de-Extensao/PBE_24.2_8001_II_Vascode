from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.exceptions import NotFound
from .models import MemberInvite
from app.user.models import User
from app.user.serializers import UserCreateSerializer
from .serializers import MemberInviteSerializer, GenerateInviteSerializer, AcceptInviteSerializer, ListInvitesSerializer, CancelInviteSerializer
import uuid
from drf_yasg.utils import swagger_auto_schema
class MemberViewSet(viewsets.ViewSet):
    # 1. Método para gerar links de convite
    @swagger_auto_schema(request_body=GenerateInviteSerializer)
    @action(detail=False, methods=['post'], url_path='generate-invite')
    def generate_invite(self, request):
        serializer = GenerateInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inviter_id = serializer.validated_data['inviter_id']
        try:
            inviter = User.objects.get(id=inviter_id)
        except User.DoesNotExist:
            raise NotFound("Usuário que está enviando o convite não foi encontrado.")
        # Verificar limite de convites (exemplo: limitar para 5 convites por usuário)
        if MemberInvite.objects.filter(inviter=inviter, is_accepted=False).count() >= 5:
            return Response({"detail": "Você já atingiu o limite de convites pendentes."}, status=status.HTTP_400_BAD_REQUEST)
        # Criação do convite
        invite_link = uuid.uuid4()
        expires_at = timezone.now() + timezone.timedelta(days=7)  # O convite expira em 7 dias
        invite = MemberInvite.objects.create(
            inviter=inviter,
            invite_link=invite_link,
            expires_at=expires_at
        )
        return Response({
            "invite_id": invite.id,
            "invite_link": str(invite.invite_link),
            "expires_at": invite.expires_at
        }, status=status.HTTP_201_CREATED)
    # 2. Método para verificar a validade do convite e aceitar
    @swagger_auto_schema(request_body=AcceptInviteSerializer)
    @action(detail=False, methods=['post'], url_path='accept-invite')
    def accept_invite(self, request):
        serializer = AcceptInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_id = serializer.validated_data['invite_id']
        try:
            invite = MemberInvite.objects.get(id=invite_id)
        except MemberInvite.DoesNotExist:
            raise NotFound("Convite não encontrado.")
        # Verifica se o convite expirou
        if invite.expires_at < timezone.now():
            return Response({"detail": "Este convite já expirou."}, status=status.HTTP_400_BAD_REQUEST)
        # Verifica se o convite já foi aceito
        if invite.is_accepted:
            return Response({"detail": "Este convite já foi aceito."}, status=status.HTTP_400_BAD_REQUEST)
        # Serializa os dados para criar o usuário
        user_data = {
            'email': serializer.validated_data['email'],
            'password': serializer.validated_data['password'],
        }
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        # Atualiza o convite
        invite.invited_user = user
        invite.is_accepted = True
        invite.save()
        return Response({"detail": "Usuário registrado com sucesso."}, status=status.HTTP_201_CREATED)
    # 3. Método para listar convites enviados
    @swagger_auto_schema(request_body=ListInvitesSerializer)
    @action(detail=False, methods=['post'], url_path='list-invites')
    def list_invites(self, request):
        serializer = ListInvitesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inviter_id = serializer.validated_data['inviter_id']
        try:
            inviter = User.objects.get(id=inviter_id)
        except User.DoesNotExist:
            raise NotFound("Usuário que está enviando o convite não foi encontrado.")
        invites = MemberInvite.objects.filter(inviter=inviter)
        invite_serializer = MemberInviteSerializer(invites, many=True)
        return Response(invite_serializer.data, status=status.HTTP_200_OK)
    # 4. Método para cancelar um convite não aceito
    @swagger_auto_schema(request_body=CancelInviteSerializer)
    @action(detail=False, methods=['post'], url_path='cancel-invite')
    def cancel_invite(self, request):
        serializer = CancelInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_id = serializer.validated_data['invite_id']
        try:
            invite = MemberInvite.objects.get(id=invite_id)
        except MemberInvite.DoesNotExist:
            raise NotFound("Convite não encontrado.")
        if invite.is_accepted:
            return Response({"detail": "O convite já foi aceito e não pode ser cancelado."}, status=status.HTTP_400_BAD_REQUEST)
        invite.delete()
        return Response({"detail": "Convite cancelado com sucesso."}, status=status.HTTP_200_OK)