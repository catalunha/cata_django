from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import (
    User,
    Variavel,
)

from .serializers import (
    UserSerializer,
    VariavelSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (DjangoModelPermissions,)

class VariavelViewSet(viewsets.ModelViewSet):
    serializer_class = VariavelSerializer
    queryset = Variavel.objects.all()
    permission_classes = (DjangoModelPermissions,)
