from rest_framework import serializers
from ..member.models import MemberInvite
class MemberInviteSerializer(serializers.ModelSerializer):
    inviter_username = serializers.ReadOnlyField(source='inviter.username')
    invited_username = serializers.SerializerMethodField()
    class Meta:
        model = MemberInvite
        fields = ['id', 'inviter', 'inviter_username', 'invite_link', 'invited_user', 'invited_username', 'created_at', 'is_accepted']
        read_only_fields = ['inviter', 'created_at', 'is_accepted']
    def get_invited_username(self, obj):
        if obj.invited_user:
            return obj.invited_user.username
        return None
    def create(self, validated_data):
        validated_data['inviter'] = self.context['request'].user
        return super().create(validated_data)
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