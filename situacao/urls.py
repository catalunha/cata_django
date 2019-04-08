from django.urls import path

from . import views

app_name = "situacao"

#path("indicenovo/", views.indicenovo, name = "indicenovo"),
urlpatterns = [
    path("indiceitem/<uuid:id>", views.indiceitem, name = "indiceitem"),
    path("indicesubitem/<uuid:id>", views.indicesubitem, name = "indicesubitem"),
    path("indiceeditar/<uuid:id>", views.indiceeditar, name = "indiceeditar"),
    path("sobe/<uuid:id>", views.sobe, name = "sobe"),
    path("desce/<uuid:id>", views.desce, name = "desce"),
    path("problemanovo/<uuid:id>", views.problemanovo, name = "problemanovo"),
    path("problemaeditar/<uuid:id>", views.problemaeditar, name = "problemaeditar"),
    path("texto/<uuid:id>", views.texto, name = "texto"),
    path("simulacao/<uuid:id>", views.simulacao, name = "simulacao"),
    path("simulacaonovo/<uuid:id>", views.simulacaonovo, name = "simulacaonovo"),
    path("simulacaoapagar/<uuid:id>", views.simulacaoapagar, name = "simulacaoapagar"),
    path("simulacaoapagartodas/<uuid:id>", views.simulacaoapagartodas, name = "simulacaoapagartodas"),
    path("simulacaoimportar/<uuid:id>", views.simulacaoimportar, name = "simulacaoimportar"),
    path("vlraleatnovo/<uuid:id>", views.vlraleatnovo, name = "vlraleatnovo"),
    path("vlraleateditar/<uuid:id>", views.vlraleateditar, name = "vlraleateditar"),
    path("respostanovo/<uuid:id>", views.respostanovo, name = "respostanovo"),
    path("respostaeditar/<uuid:id>", views.respostaeditar, name = "respostaeditar"),
    path("textonovo/<uuid:id>", views.textonovo, name = "textonovo"),
    path("textoeditar/<uuid:id>", views.textoeditar, name = "textoeditar"),
    path("anexonovo/<uuid:id>", views.anexonovo, name = "anexonovo"),
    path("anexoeditar/<uuid:id>", views.anexoeditar, name = "anexoeditar"),
    path("apagar/<uuid:id>", views.apagar, name = "apagar"),
    path("programanovo/<uuid:id>", views.programanovo, name = "programanovo"),
    path("programaeditar/<uuid:id>", views.programaeditar, name = "programaeditar"),
    path("propostaeditar/<uuid:id>", views.propostaeditar, name = "propostaeditar"),
    path("proposta/<uuid:id>", views.proposta, name = "proposta"),
    path("testenovo/<uuid:id>", views.testenovo, name = "testenovo"),
    path("testeeditar/<uuid:id>", views.testeeditar, name = "testeeditar"),
]
