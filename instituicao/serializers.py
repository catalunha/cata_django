from rest_framework import serializers
from painel.mixins import ArquivoBase64SerializerField
from instituicao.models import Instituicao,Conhecimento,Turma


class InstituicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = '__all__'


class ConhecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conhecimento
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'
