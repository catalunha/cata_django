from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import (
    Instituicao,
    Conhecimento,
    Turma,
)

from .serializers import (
    InstituicaoSerializer,
    ConhecimentoSerializer,
    TurmaSerializer,
)

class InstituicaoViewSet(viewsets.ModelViewSet):
    serializer_class = InstituicaoSerializer
    queryset = Instituicao.objects.all()
    permission_classes = (DjangoModelPermissions,)

class ConhecimentoViewSet(viewsets.ModelViewSet):
    serializer_class = ConhecimentoSerializer
    queryset = Conhecimento.objects.all()
    permission_classes = (DjangoModelPermissions,)

class TurmaViewSet(viewsets.ModelViewSet):
    serializer_class = TurmaSerializer
    queryset = Turma.objects.all()
    permission_classes = (DjangoModelPermissions,)
