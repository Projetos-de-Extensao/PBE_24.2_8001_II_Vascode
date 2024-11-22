from django.contrib import admin
from .models import ProductFeedback

# Registrando o modelo ProductFeedback para aparecer no painel administrativo
admin.site.register(ProductFeedback)
