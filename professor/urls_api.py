from django.urls import path, include
from rest_framework import routers

from .views_api import (
    EmentaViewSet,
    QuestaoStatusViewSet,
    AlgoritmoStatusViewSet,
)

instituicao_router = routers.DefaultRouter()

instituicao_router.register(r'ementa', EmentaViewSet)
instituicao_router.register(r'questaoStatus', QuestaoStatusViewSet)
instituicao_router.register(r'algoritmoStatus', AlgoritmoStatusViewSet)

urlpatterns = [
    path('', include(instituicao_router.urls)),
]
