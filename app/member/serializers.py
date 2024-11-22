from rest_framework import serializers
from ..member.models import MemberInvite
from django.contrib.auth.models import User

class MemberInviteSerializer(serializers.ModelSerializer):
    inviter_username = serializers.ReadOnlyField(source='inviter.username')
    invited_username = serializers.SerializerMethodField()
    invite_link = serializers.SerializerMethodField()

    class Meta:
        model = MemberInvite
        fields = ['id', 'inviter', 'inviter_username', 'invite_link', 'invited_user', 'invited_username', 'created_at', 'expires_at', 'is_accepted']
        read_only_fields = ['inviter', 'created_at', 'expires_at', 'is_accepted']

class GenerateInviteSerializer(serializers.Serializer):
    inviter_id = serializers.IntegerField()


class AcceptInviteSerializer(serializers.Serializer):
    invite_id = serializers.UUIDField()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

class ListInvitesSerializer(serializers.Serializer):
    inviter_id = serializers.IntegerField()

class CancelInviteSerializer(serializers.Serializer):
    invite_id = serializers.UUIDField()
