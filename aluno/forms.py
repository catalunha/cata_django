# -*- coding: utf8 -*-
from django import forms

class CodigoForm(forms.Form):
    entrada = forms.CharField(label='entrada.txt',required=False,widget=forms.Textarea,help_text='Cada linha simula a entrada de um valor via teclado.')
    interface = forms.CharField(label='interface.dart',required=False,widget=forms.Textarea,help_text='Na área acima digite o código que recebe os dados, chama a classe criada em solucao.dart e imprime os resultados.')
    solucao = forms.CharField(label='solucao.dart',required=False,widget=forms.Textarea,help_text='Na área acima digite a classe que recebe os valores, realiza os cálculo e fornece o resultado.')
    dados = forms.CharField(label='dados.txt',required=False,widget=forms.Textarea,help_text='Caso necessário a entrada de dados pode ser via arquivo.')
