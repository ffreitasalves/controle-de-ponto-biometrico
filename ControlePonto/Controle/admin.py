# -*- coding:utf-8 -*-
import time, datetime
from datetime import *
from models import *
from django.contrib import admin
from django import forms
from django.db import models
from widgets import impressao
from views import bancohoras
from django.conf.urls.defaults import *

class EnderecosInLine(admin.StackedInline):
    model = Endereco
    extra = 1
    max_num=3
    fieldsets=(
        (None, {
            'fields':(('Logradouro','Numero','Complemento'),('Bairro','CEP'),('Cidade','Estado'),('DDD','Telefone'),),
            }),        
        )

class CelularesInLine(admin.TabularInline):
    model = Celular
    max_num=3
    extra=1

class HorarioFixoInLine(admin.TabularInline):
    model= HorarioFixo
    extra=5

class OcupadaInLine(admin.TabularInline):
    model = Ocupada
    extra=1
    max_num=2

class BancoHorasInLine(admin.TabularInline):
    model = BancoHoras
    max_num = 1

    
class EstagiarioAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('Estagiario','Ativo',)
    list_filter=('Ativo',)    
    class Media:
        js = ("js/fingerprint.js","js/jquery.js",)
    
    formfield_overrides = {
        models.TextField : {'widget': impressao()},
        
    }
    
    fieldsets =  (
        (None, { 'fields': (('NUSP','Estagiario','Usuario_ad'),('Unidade','Curso','Ingresso'),('CPF','RG','Email'),('Ativo'),('Foto'),('Impressao')),}),
        ('Informacoes Bancarias', {'fields':(('Ag','Conta','Banco'),),}),
        )
    def get_urls(self):
        urls = super(EstagiarioAdmin,self).get_urls()
        url_banco_horas = patterns('',
            (r'^relatorios/BancoHoras/$', bancohoras), 
        )
        return urls + url_banco_horas
    inlines = [EnderecosInLine,
               CelularesInLine,
               HorarioFixoInLine,
               OcupadaInLine,
               BancoHorasInLine,
               ]

class RegistroPontoAdmin(admin.ModelAdmin):
    list_display=('Estagiario','Data','Entrada','Saida','Aceito',)
    list_display_links=('Estagiario',)
    list_filter=('Estagiario','Data','Aceito',)
    

class EstornoDeHorario(RegistroPonto):
    class Meta:
        proxy=True
        verbose_name = u'Estorno de Horario'
        verbose_name_plural =  (u'Estorno de Horarios (%s)' % RegistroPonto.objects.filter(Aceito=False).count())
        ordering= ["-Data","-Entrada"]

class EstornoAdmin(admin.ModelAdmin):
    list_display=('Estagiario','Data_f','Entrada_f','Saida_f','Aceito',)
    list_display_links=('Estagiario',)
     
    
    def Data_f(self,obj):
        return obj.Data.strftime("%d/%m/%Y")
    Data_f.short_description = "Data"
    
    def Entrada_f(self,obj):
        return obj.Entrada.strftime("%H:%M")
    Entrada_f.short_description = "Entrada"

    def Saida_f(self,obj):
        if obj.Saida:
            return obj.Saida.strftime("%H:%M")
        else:
            return ''
    Saida_f.short_description = "Saida"
    
    def queryset(self, request):
        qs = super(EstornoAdmin,self).queryset(request)
        return qs.filter(Aceito=False)



        

admin.site.register(Estagiario,EstagiarioAdmin)
admin.site.register(Curso)
admin.site.register(Vaga)
admin.site.register(Ocupada)
admin.site.register(Tipo_Vaga)
admin.site.register(Feriado)
admin.site.register(RegistroPonto, RegistroPontoAdmin)
admin.site.register(EstornoDeHorario, EstornoAdmin)
