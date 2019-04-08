from django.urls import path

from . import views

app_name = "painel"

urlpatterns = [
    path("", views.index, name = "index"),
    path("sair/", views.sair, name = "sair"),
    path("alunonovo/<uuid:id>", views.alunonovo, name = "alunonovo"),
    path("alunoeditar/<uuid:id>", views.alunoeditar, name = "alunoeditar"),
    path("senhanova/", views.senhanova, name = "senhanova"),
    path("senhareset/<uuid:id>", views.senhareset, name = "senhareset"),
]
