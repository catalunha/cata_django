from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from api.views import VersaoAPIView

app_name = 'api'

urlpatterns = [
    path('versao/', VersaoAPIView.as_view(), name='versao'),
    path('auth/', include('api.urls_auth')),
    path('docs/', include('api.urls_docs')),

    path('instituicao/', include('instituicao.urls_api')),
    path('painel/', include('painel.urls_api')),
    path('professor/', include('professor.urls_api')),
    path('situacao/', include('situacao.urls_api')),
    path('tarefa/', include('tarefa.urls_api')),

]
