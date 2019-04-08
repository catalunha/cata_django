from django.contrib import admin
from painel.models import User

from instituicao.models import Instituicao,Conhecimento,Turma

class InstituicaoAdmin(admin.ModelAdmin):
    list_display=('nome','descricao',)
    fields=('nome','descricao',)
admin.site.register(Instituicao,InstituicaoAdmin)

class ConhecimentoAdmin(admin.ModelAdmin):
    list_display=('id','usuario','nome','ativo','descricao','inicio','fim','instituicao',)
    fields=('usuario','nome','ativo','descricao','inicio','fim','instituicao',)
admin.site.register(Conhecimento,ConhecimentoAdmin)

class TurmaAdmin(admin.ModelAdmin):
    list_display=('ativo','conhecimento','nome','questao','descricao','inicio','fim','alunos_mm',)
    fields=('ativo','conhecimento','nome','descricao','inicio','fim','alunos',)
admin.site.register(Turma,TurmaAdmin)
