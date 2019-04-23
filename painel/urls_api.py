from django.urls import path, include
from rest_framework import routers

from .views_api import (
    UserViewSet,
    VariavelViewSet,
)

painel_router = routers.DefaultRouter()

painel_router.register(r'user', UserViewSet)
painel_router.register(r'variavel', VariavelViewSet)

urlpatterns = [
    path('', include(painel_router.urls)),
]
