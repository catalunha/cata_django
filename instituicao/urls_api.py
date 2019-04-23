from django.urls import path, include
from rest_framework import routers

from .views_api import (
    InstituicaoViewSet,
    ConhecimentoViewSet,
    TurmaViewSet,
)

instituicao_router = routers.DefaultRouter()

instituicao_router.register(r'instituicao', InstituicaoViewSet)
instituicao_router.register(r'conhecimento', ConhecimentoViewSet)
instituicao_router.register(r'turma', TurmaViewSet)

urlpatterns = [
    path('', include(instituicao_router.urls)),
]
