from django.contrib import admin
from painel.models import User

from tarefa.models import Avaliacao,Questao,Aplicada,Solucao,Relatorio,Anexo,Algoritmo,Codigo,Aplicado

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display=("id","ativo",'turma','nome','privada','inicio','fim',)
admin.site.register(Avaliacao,AvaliacaoAdmin)

def avaliacaoid(obj):
    return "{}".format(obj.avaliacao.id)
avaliacaoid.short_description = 'AvalID'

class QuestaoAdmin(admin.ModelAdmin):
    list_display=('id',"ativo",'avaliacao',avaliacaoid,'problema','numero','tentativa','tempo','nota',)
admin.site.register(Questao,QuestaoAdmin)

class AplicadaAdmin(admin.ModelAdmin):
    list_display=("id",'ativo',"usuario",'questao',)
admin.site.register(Aplicada,AplicadaAdmin)

class SolucaoAdmin(admin.ModelAdmin):
    list_display=("ativo",'aplicada','resposta','solucao','nota',)
admin.site.register(Solucao,SolucaoAdmin)

class RelatorioAdmin(admin.ModelAdmin):
    list_display=("ativo",'aplicada','texto','relatorio','nota',)
admin.site.register(Relatorio,RelatorioAdmin)

class AnexoAdmin(admin.ModelAdmin):
    list_display=("ativo",'aplicada','arquivo','anexo','nota',)
admin.site.register(Anexo,AnexoAdmin)

class AlgoritmoAdmin(admin.ModelAdmin):
    list_display=("ativo",'avaliacao','programa','tempo','nota',)
admin.site.register(Algoritmo,AlgoritmoAdmin)

class AplicadoAdmin(admin.ModelAdmin):
    list_display=("id","usuario",'algoritmo',)
admin.site.register(Aplicado,AplicadoAdmin)

class CodigoAdmin(admin.ModelAdmin):
    list_display=("ativo",'aplicado','proposta','conteudo','nota',)
admin.site.register(Codigo,CodigoAdmin)
