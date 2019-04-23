from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import (
    Ementa,
    QuestaoStatus,
    AlgoritmoStatus,
)

from .serializers import (
    EmentaSerializer,
    QuestaoStatusSerializer,
    AlgoritmoStatusSerializer,
)

class EmentaViewSet(viewsets.ModelViewSet):
    serializer_class = EmentaSerializer
    queryset = Ementa.objects.all()
    permission_classes = (DjangoModelPermissions,)

class QuestaoStatusViewSet(viewsets.ModelViewSet):
    serializer_class = QuestaoStatusSerializer
    queryset = QuestaoStatus.objects.all()
    permission_classes = (DjangoModelPermissions,)

class AlgoritmoStatusViewSet(viewsets.ModelViewSet):
    serializer_class = AlgoritmoStatusSerializer
    queryset = AlgoritmoStatus.objects.all()
    permission_classes = (DjangoModelPermissions,)
