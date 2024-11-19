from django.db import models
from app.user.models import User
from django.utils import timezone
import datetime
class MemberInvite(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    invite_link = models.CharField(max_length=255, unique=True)
    invited_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='invite', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=7))  # Valor padrão
    is_accepted = models.BooleanField(default=False)
    def __str__(self):
        return f"Invite from {self.inviter.username} to {'Pending' if not self.invited_user else self.invited_user.username}"
    def is_expired(self):
        return timezone.now() > self.expires_at