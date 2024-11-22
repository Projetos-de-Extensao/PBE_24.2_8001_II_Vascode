from rest_framework import serializers
from django.contrib.auth.models import User

# Serializer para criação de usuários
class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()  # Inclui o campo `id` apenas para leitura
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'first_name', 'last_name']


# Serializer para atualização de usuários
class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()  # Inclui o campo `id` apenas para leitura
    password = serializers.CharField(write_only=True, min_length=8, max_length=128, required=False)

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'first_name', 'last_name']