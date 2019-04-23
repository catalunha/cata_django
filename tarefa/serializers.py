from rest_framework import serializers
from painel.mixins import ArquivoBase64SerializerField
from tarefa.models import Avaliacao,Questao,Aplicada,Solucao,Relatorio,Anexo,Algoritmo,Codigo,Aplicado


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'

class QuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questao
        fields = '__all__'

class AplicadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aplicada
        fields = '__all__'

class SolucaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solucao
        fields = '__all__'

class RelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = '__all__'

class AnexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo
        fields = '__all__'

class AlgoritmoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algoritmo
        fields = '__all__'

class CodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigo
        fields = '__all__'


class AplicadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aplicado
        fields = '__all__'

