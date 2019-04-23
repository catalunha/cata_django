from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from .models import (
    Indice,
    Problema,
    Simulacao,
    ValorAleatorio,
    Resposta,
    Arquivo,
    Texto,
    Programa,
    Proposta,
    Teste,
)

from .serializers import (
    IndiceSerializer,
    ProblemaSerializer,
    SimulacaoSerializer,
    ValorAleatorioSerializer,
    RespostaSerializer,
    ArquivoSerializer,
    TextoSerializer,
    ProgramaSerializer,
    PropostaSerializer,
    TesteSerializer,
)

class IndiceViewSet(viewsets.ModelViewSet):
    serializer_class = IndiceSerializer
    queryset = Indice.objects.all()
    permission_classes = (DjangoModelPermissions,)

class ProblemaViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemaSerializer
    queryset = Problema.objects.all()
    permission_classes = (DjangoModelPermissions,)

class SimulacaoViewSet(viewsets.ModelViewSet):
    serializer_class = SimulacaoSerializer
    queryset = Simulacao.objects.all()
    permission_classes = (DjangoModelPermissions,)

class ValorAleatorioViewSet(viewsets.ModelViewSet):
    serializer_class = ValorAleatorioSerializer
    queryset = ValorAleatorio.objects.all()
    permission_classes = (DjangoModelPermissions,)

class RespostaViewSet(viewsets.ModelViewSet):
    serializer_class = RespostaSerializer
    queryset = Resposta.objects.all()
    permission_classes = (DjangoModelPermissions,)

class ArquivoViewSet(viewsets.ModelViewSet):
    serializer_class = ArquivoSerializer
    queryset = Arquivo.objects.all()
    permission_classes = (DjangoModelPermissions,)

class TextoViewSet(viewsets.ModelViewSet):
    serializer_class = TextoSerializer
    queryset = Texto.objects.all()
    permission_classes = (DjangoModelPermissions,)

class ProgramaViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramaSerializer
    queryset = Programa.objects.all()
    permission_classes = (DjangoModelPermissions,)

class PropostaViewSet(viewsets.ModelViewSet):
    serializer_class = PropostaSerializer
    queryset = Proposta.objects.all()
    permission_classes = (DjangoModelPermissions,)

class TesteViewSet(viewsets.ModelViewSet):
    serializer_class = TesteSerializer
    queryset = Teste.objects.all()
    permission_classes = (DjangoModelPermissions,)
