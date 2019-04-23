from rest_framework import serializers
from painel.mixins import ArquivoBase64SerializerField
from professor.models import Ementa, QuestaoStatus, AlgoritmoStatus

class EmentaSerializer(serializers.ModelSerializer):
    texto = ArquivoBase64SerializerField()
    class Meta:
        model = Ementa
        fields = '__all__'

class QuestaoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestaoStatus
        fields = '__all__'

class AlgoritmoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlgoritmoStatus
        fields = '__all__'

