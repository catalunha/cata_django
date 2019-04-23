from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import (
    Avaliacao,
    Questao,
    Aplicada,
    Solucao,
    Relatorio,
    Anexo,
    Algoritmo,
    Codigo,
    Aplicado,
)

from .serializers import (
    AvaliacaoSerializer,
    QuestaoSerializer,
    AplicadaSerializer,
    SolucaoSerializer,
    RelatorioSerializer,
    AnexoSerializer,
    AlgoritmoSerializer,
    CodigoSerializer,
    AplicadoSerializer,
)

class AvaliacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AvaliacaoSerializer
    queryset = Avaliacao.objects.all()
    permission_classes = (DjangoModelPermissions,)

class QuestaoViewSet(viewsets.ModelViewSet):
    serializer_class = QuestaoSerializer
    queryset = Questao.objects.all()
    permission_classes = (DjangoModelPermissions,)

class AplicadaViewSet(viewsets.ModelViewSet):
    serializer_class = AplicadaSerializer
    queryset = Aplicada.objects.all()
    permission_classes = (DjangoModelPermissions,)

class SolucaoViewSet(viewsets.ModelViewSet):
    serializer_class = SolucaoSerializer
    queryset = Solucao.objects.all()
    permission_classes = (DjangoModelPermissions,)

class RelatorioViewSet(viewsets.ModelViewSet):
    serializer_class = RelatorioSerializer
    queryset = Relatorio.objects.all()
    permission_classes = (DjangoModelPermissions,)

class AnexoViewSet(viewsets.ModelViewSet):
    serializer_class = AnexoSerializer
    queryset = Anexo.objects.all()
    permission_classes = (DjangoModelPermissions,)

class AlgoritmoViewSet(viewsets.ModelViewSet):
    serializer_class = AlgoritmoSerializer
    queryset = Algoritmo.objects.all()
    permission_classes = (DjangoModelPermissions,)

class CodigoViewSet(viewsets.ModelViewSet):
    serializer_class = CodigoSerializer
    queryset = Codigo.objects.all()
    permission_classes = (DjangoModelPermissions,)

class AplicadoViewSet(viewsets.ModelViewSet):
    serializer_class = AplicadoSerializer
    queryset = Aplicado.objects.all()
    permission_classes = (DjangoModelPermissions,)
