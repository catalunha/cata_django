# -*- coding: utf8 -*-
from django import forms

from tarefa.models import Avaliacao,Questao,Aplicada,Solucao,Relatorio,Anexo,Algoritmo,Codigo,Aplicado
from instituicao.models import Conhecimento,Turma
from situacao.models import Indice,Problema,Simulacao,ValorAleatorio,Resposta,Arquivo,Texto,Programa,Teste

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields=['nome','inicio','fim','privada','ativo','nota',]

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields=['problema','ativo','tentativa','tempo','nota',]
    def __init__(self, user, avaliacao, *args, **kwargs):
        super(QuestaoForm, self).__init__(*args, **kwargs)
        self.fields['problema'].queryset = Problema.objects.filter(usuario=user,ativo=True,indices__in=avaliacao.turma.conhecimento.indices.all())

class AlgoritmoForm(forms.ModelForm):
    class Meta:
        model = Algoritmo
        fields=['programa','ativo','tempo','nota',]
    def __init__(self, user, avaliacao, *args, **kwargs):
        super(AlgoritmoForm, self).__init__(*args, **kwargs)
        self.fields['programa'].queryset = Programa.objects.filter(usuario=user,ativo=True,indices__in=avaliacao.turma.conhecimento.indices.all())
