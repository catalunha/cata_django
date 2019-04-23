from django.urls import path, include
from rest_framework import routers

from .views_api import (
    IndiceViewSet,
    ProblemaViewSet,
    SimulacaoViewSet,
    ValorAleatorioViewSet,
    RespostaViewSet,
    ArquivoViewSet,
    TextoViewSet,
    ProgramaViewSet,
    PropostaViewSet,
    TesteViewSet,
)

situacao_router = routers.DefaultRouter()

situacao_router.register(r'indice', IndiceViewSet)
situacao_router.register(r'problema', ProblemaViewSet)
situacao_router.register(r'simulacao', SimulacaoViewSet)
situacao_router.register(r'valorAleatorio', ValorAleatorioViewSet)
situacao_router.register(r'resposta', RespostaViewSet)
situacao_router.register(r'arquivo', ArquivoViewSet)
situacao_router.register(r'texto', TextoViewSet)
situacao_router.register(r'programa', ProgramaViewSet)
situacao_router.register(r'proposta', PropostaViewSet)
situacao_router.register(r'teste', TesteViewSet)

urlpatterns = [
    path('', include(situacao_router.urls)),
]
