from rest_framework import serializers
from painel.mixins import ArquivoBase64SerializerField
from situacao.models import Indice,Problema,Simulacao,ValorAleatorio,Resposta,Arquivo,Texto,Programa,Proposta,Teste

class IndiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indice
        fields = '__all__'

class ProblemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problema
        fields = '__all__'

class SimulacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulacao
        fields = '__all__'

class ValorAleatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValorAleatorio
        fields = '__all__'

class RespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resposta
        fields = '__all__'

class ArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arquivo
        fields = '__all__'

class TextoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texto
        fields = '__all__'

class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = '__all__'

class PropostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposta
        fields = '__all__'

class TesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teste
        fields = '__all__'
