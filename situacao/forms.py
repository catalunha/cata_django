# -*- coding: utf8 -*-
from django import forms

from situacao.models import Indice,Problema,Simulacao,ValorAleatorio,Resposta,Arquivo,Texto,Programa,Proposta,Teste
from instituicao.models import Conhecimento,Turma
'''
class IndiceForm(forms.ModelForm):
    class Meta:
        model = Indice
        fields=['conhecimento','nome','superior','descricao',]
    def __init__(self, user, *args, **kwargs):
        super(IndiceForm, self).__init__(*args, **kwargs)
        self.fields['conhecimento'].queryset = Conhecimento.objects.filter(usuario=user,ativo=True)
        self.fields['superior'].queryset = Indice.objects.filter(conhecimento__usuario=user,conhecimento__ativo=True)
'''
class IndiceForm(forms.ModelForm):
    class Meta:
        model = Indice
        #fields=['nome','descricao','conhecimento','superior',]
        fields=['nome','descricao']

class Indice2Form(forms.ModelForm):
    class Meta:
        model = Indice
        #fields=['nome','descricao','conhecimento','superior',]
        fields=['nome','descricao','superior',]
    def __init__(self,*args, **kwargs):
        super(Indice2Form, self).__init__(*args, **kwargs)
        indice = kwargs.pop("instance")
        filhos = indice.get_arvore_genealogica()
        queryset = Indice.objects.exclude(pk__in = [filho.pk for filho in filhos])
        self.fields["superior"].queryset = queryset

class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        fields=['referencia','descricao','pdf','ativo','proposta','solucao','observacao',]

class Problema2Form(forms.ModelForm):
    class Meta:
        model = Problema
        fields=['referencia','descricao','pdf','ativo','proposta','solucao','observacao','indices',]

class ValorAleatorioForm(forms.ModelForm):
    class Meta:
        model = ValorAleatorio
        fields=['nome','valor',]


class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields=['letra','valor',]

class TextoForm(forms.ModelForm):
    class Meta:
        model = Texto
        fields=['letra','texto',]

class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields=['letra','arquivo',]

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields=['referencia','descricao','pdf','ativo','observacao']
class Programa2Form(forms.ModelForm):
    class Meta:
        model = Programa
        fields=['referencia','descricao','pdf','ativo','observacao','indices',]

class PropostaForm(forms.ModelForm):
    class Meta:
        model = Proposta
        fields=['conteudo',]


class TesteForm(forms.ModelForm):
    class Meta:
        model = Teste
        fields=['entrada','saida',]
