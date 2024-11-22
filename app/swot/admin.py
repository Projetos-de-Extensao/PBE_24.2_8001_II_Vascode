from django.contrib import admin
from .models import SWOTAnalysis

# Registrando o modelo SWOTAnalysis para aparecer no painel administrativo
admin.site.register(SWOTAnalysis)