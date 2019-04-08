from django.urls import path

from . import views

app_name = "aluno"

urlpatterns = [
    path("atuais/", views.atuais, name = "atuais"),
    path("todas/", views.todas, name = "todas"),
    path("editar/<uuid:id>", views.editar, name = "editar"),
    path("editaralgoritmo/<uuid:id>", views.editaralgoritmo, name = "editaralgoritmo"),
    path("publica", views.publica, name = "publica"),
]
