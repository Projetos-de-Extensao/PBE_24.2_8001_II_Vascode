from django.contrib import admin
from .models import User

# Registrando o modelo User para aparecer no painel administrativo
admin.site.register(User)
