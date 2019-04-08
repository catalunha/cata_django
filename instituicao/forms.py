# -*- coding: utf8 -*-
from django import forms
from django.forms.widgets import TextInput, DateInput, DateTimeInput, TimeInput

from instituicao.models import Conhecimento,Turma
from painel.models import User

class DateInput(forms.DateInput):
    input_type = 'datetime-local'

class ConhecimentoForm(forms.ModelForm):
    class Meta:
        model = Conhecimento
        fields=['nome','instituicao','ativo','descricao','inicio','fim',]

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields=['nome','ativo','descricao','inicio','fim',]
