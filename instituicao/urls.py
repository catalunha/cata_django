from django.urls import path

from . import views

app_name = "instituicao"

urlpatterns = [
    path("conhecimentonovo/", views.conhecimentonovo, name = "conhecimentonovo"),
    path("conhecimentoeditar/<uuid:id>", views.conhecimentoeditar, name = "conhecimentoeditar"),
    path("turmanovo/<uuid:id>", views.turmanovo, name = "turmanovo"),
    path("turmaeditar/<uuid:id>", views.turmaeditar, name = "turmaeditar"),
    path("notas/<uuid:id>", views.notas, name = "notas"),
    path("apagar/<uuid:id>", views.apagar, name = "apagar"),
]
