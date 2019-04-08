from django.urls import path

from . import views

app_name = "professor"

urlpatterns = [
    path("acoes/", views.acoes, name = "acoes"),
    path("conhecimento/", views.conhecimento, name = "conhecimento"),
    path("indice/", views.indice, name = "indice"),
    path("notas/", views.notas, name = "notas"),
    path("alunotarefas/<uuid:idturma>/<uuid:idaluno>", views.alunotarefas, name = "alunotarefas"),
    path("ementa/", views.ementa, name = "ementa"),
    path("ementaeditar/<uuid:id>", views.ementaeditar, name = "ementaeditar"),
]
