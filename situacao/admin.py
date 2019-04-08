from django.contrib import admin
from painel.models import User

from situacao.models import Indice,Problema,Simulacao,ValorAleatorio,Resposta,Arquivo,Texto,Programa,Proposta,Teste

class IndiceAdmin(admin.ModelAdmin):
    list_display=('conhecimento','ordem','nome','superior','descricao',)
admin.site.register(Indice,IndiceAdmin)

class ProblemaAdmin(admin.ModelAdmin):
    list_display=('id','usuario','referencia','descricao','ativo','pdf','observacao','indices_mm')
admin.site.register(Problema,ProblemaAdmin)

class SimulacaoAdmin(admin.ModelAdmin):
    list_display=('id','problema',)
admin.site.register(Simulacao,SimulacaoAdmin)

class ValorAleatorioAdmin(admin.ModelAdmin):
    list_display=('id','simulacao','nome','valor',)
admin.site.register(ValorAleatorio,ValorAleatorioAdmin)

class RespostaAdmin(admin.ModelAdmin):
    list_display=('id','simulacao','letra','valor',)
admin.site.register(Resposta,RespostaAdmin)

class TextoAdmin(admin.ModelAdmin):
    list_display=('id','simulacao','letra','texto',)
admin.site.register(Texto,TextoAdmin)

class ArquivoAdmin(admin.ModelAdmin):
    list_display=('id','simulacao','letra','arquivo',)
admin.site.register(Arquivo,ArquivoAdmin)

class ProgramaAdmin(admin.ModelAdmin):
    list_display=('id','referencia','descricao','ativo','observacao','indices_mm','pdf',)
admin.site.register(Programa,ProgramaAdmin)

class PropostaAdmin(admin.ModelAdmin):
    list_display=('id','programa','arquivo','conteudo','ativo',)
admin.site.register(Proposta,PropostaAdmin)

class TesteAdmin(admin.ModelAdmin):
    list_display=('id','programa','entrada','saida',)
admin.site.register(Teste,TesteAdmin)
