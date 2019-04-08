from django.urls import path


from . import views

app_name = "tarefa"

urlpatterns = [
    path("avaliacaonovo/<uuid:id>", views.avaliacaonovo, name = "avaliacaonovo"),
    path("avaliacaoeditar/<uuid:id>", views.avaliacaoeditar, name = "avaliacaoeditar"),
    path("questaonovo/<uuid:id>", views.questaonovo, name = "questaonovo"),
    path("questaoeditar/<uuid:id>", views.questaoeditar, name = "questaoeditar"),
    path("relatoriocorrigir1/<uuid:id>", views.relatoriocorrigir1, name = "relatoriocorrigir1"),
    path("relatoriocorrigir2/", views.relatoriocorrigir2, name = "relatoriocorrigir2"),
    path("anexocorrigir1/<uuid:id>", views.anexocorrigir1, name = "anexocorrigir1"),
    path("anexocorrigir2/", views.anexocorrigir2, name = "anexocorrigir2"),
    path("aplicadaeditar/<uuid:id>", views.aplicadaeditar, name = "aplicadaeditar"),
    path("aplicadoeditar/<uuid:id>", views.aplicadoeditar, name = "aplicadoeditar"),
    path("avaliacaoaplicar1/<uuid:id>", views.avaliacaoaplicar1, name = "avaliacaoaplicar1"),
    path("avaliacaoaplicar2/<uuid:id>", views.avaliacaoaplicar2, name = "avaliacaoaplicar2"),
    path("relatorio/<uuid:id>", views.relatorio, name = "relatorio"),
    path("apagar/<uuid:id>", views.apagar, name = "apagar"),
    path("algoritmonovo/<uuid:id>", views.algoritmonovo, name = "algoritmonovo"),
    path("algoritmoeditar/<uuid:id>", views.algoritmoeditar, name = "algoritmoeditar"),
    path("codigo/<uuid:id>", views.codigo, name = "codigo"),
    path("codigocorrigir1/<uuid:id>", views.codigocorrigir1, name = "codigocorrigir1"),
    path("codigocorrigir2/", views.codigocorrigir2, name = "codigocorrigir2"),
    path("codigotestar/<uuid:id>", views.codigotestar, name = "codigotestar"),
    path("valoresaleatoriosver/<uuid:id>", views.valoresaleatoriosver, name = "valoresaleatoriosver"),
]
