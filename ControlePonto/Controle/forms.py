# -*- coding:utf-8 -*-
from django import forms
from models import Estagiario



class HorariosFeitos(forms.Form):
    listaests = [[0, 'Selecionar Todos']]
    for est in Estagiario.objects.filter(Ativo=True):        
        listaests.append([est.id, est.Estagiario.title()])
    ests = forms.MultipleChoiceField(
        choices=listaests,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Estagiarios')
    
    De = forms.DateField()
    Ate = forms.DateField()
    class Media:
        js = ('js/jquery.js','js/jquery.click-calendario-1.0.js',)
        css = {
            'all':('css/jquery.click-calendario-1.0.css',)
            }
