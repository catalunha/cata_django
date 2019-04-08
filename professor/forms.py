# -*- coding: utf8 -*-
from django import forms

from professor.models import Ementa

class EmentaForm(forms.ModelForm):
	class Meta:
		model = Ementa
		fields=['texto',]
		widgets = {
          'texto': forms.Textarea(attrs={'rows':50, 'cols':120}),
        }
