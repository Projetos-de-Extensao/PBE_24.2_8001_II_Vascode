from django.contrib import admin
from .models import MemberInvite

# Registrando o modelo MemberInvite para aparecer no painel administrativo
admin.site.register(MemberInvite)