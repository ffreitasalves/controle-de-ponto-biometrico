# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from Controle.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^Ponto/', include('ControlePonto.foo.urls')),
    (r'^$', index), # Pagina com o botao Registrar Horario
    (r'^Registro/$', registro), # Insere o RegistroTrabalho
    (r'^registro/$', registro), # Insere o RegistroTrabalho
    (r'^Relatorios/$', relatorios), # Exibe os relatorios
    (r'^relatorios/$', relatorios), # Exibe os relatorios
    (r'^Relatorios/horariofixo/$', horarios), # Mostra a tabela com o horario de todos os estagiarios.
    (r'^relatorios/horariofixo/$', horarios), # Mostra a tabela com o horario de todos os estagiarios.
    (r'^Relatorios/horariosfeitos/$', horariosfiltro), # Mostra uma pagina com o filtro para a hora dos estagiarios
    (r'^relatorios/horariosfeitos/$', horariosfiltro), # Mostra uma pagina com o filtro para a hora dos estagiarios
    (r'^relatorios/horariosfeitos/(?P<hor_id>\d+)/$', acceptid), # Mostra uma pagina com o filtro para a hora dos estagiarios                  
    (r'^Relatorios/bancohoras/$', bancohoras), #BancoHoras
    (r'^relatorios/bancohoras/$', bancohoras), #BancoHoras
    (r'^relatorios/ranking/$', ranking), #BancoHoras
    (r'^entrar/$', 'django.contrib.auth.views.login', {'template_name': 'entrar.html'}, 'entrar'),
    (r'^sair/$', 'django.contrib.auth.views.logout'),



    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/HorariosFeitos', admin.site.admin_view(horariosfiltro)),
    (r'^admin/', include(admin.site.urls)),

    # Url de Media
    (r'^media2/(.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
