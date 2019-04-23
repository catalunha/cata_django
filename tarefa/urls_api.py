from django.urls import path, include
from rest_framework import routers

from .views_api import (
    AvaliacaoViewSet,
    QuestaoViewSet,
    AplicadaViewSet,
    SolucaoViewSet,
    RelatorioViewSet,
    AnexoViewSet,
    AlgoritmoViewSet,
    CodigoViewSet,
    AplicadoViewSet,
)
tarefa_router = routers.DefaultRouter()

tarefa_router.register(r'avaliacao', AvaliacaoViewSet)
tarefa_router.register(r'questao', QuestaoViewSet)
tarefa_router.register(r'aplicada', AplicadaViewSet)
tarefa_router.register(r'solucao', SolucaoViewSet)
tarefa_router.register(r'relatorio', RelatorioViewSet)
tarefa_router.register(r'anexo', AnexoViewSet)
tarefa_router.register(r'algoritmo', AlgoritmoViewSet)
tarefa_router.register(r'codigo', CodigoViewSet)
tarefa_router.register(r'aplicado', AplicadoViewSet)

urlpatterns = [
    path('', include(tarefa_router.urls)),
]
