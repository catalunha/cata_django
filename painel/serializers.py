from rest_framework import serializers
from painel.mixins import ArquivoBase64SerializerField
from painel.models import User,Variavel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "last_login",
            "is_superuser",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "username",
            "first_name",
            "groups",
            "user_permissions",
            "cargo",
            "professor",
        )

class VariavelSerializer(serializers.ModelSerializer):
    arquivo = ArquivoBase64SerializerField()
    class Meta:
        model = Variavel
        fields = '__all__'
