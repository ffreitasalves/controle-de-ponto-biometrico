# -*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from models import Estagiario, RegistroPonto, HorarioFixo, BancoHoras, Feriado, Ocupada
from decimal import *
from forms import HorariosFeitos
from datetime import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template import Context, loader
from django.template import RequestContext
from classes import urls_type, estbank_type


def index(request):    
    #Montando os campos de pesquisa.
    campos =[]
    op_estado={0:"",1:"Entrou",2:"Saiu"}
    for e in Estagiario.objects.filter(Ativo=True):
        campos.append('<input type=hidden id="id_bd" name="%s" value=%s />' % (e.id , e.Impressao))

    est = request.GET.get('est',0)
    estado = int( request.GET.get('estado',0))
    estado = op_estado.get(estado)

    if est==0 or estado ==0:
        func = ""
    else:
        try:
            estag = Estagiario.objects.get(pk=est)
            func = "%s %s" % (estag , estado)        
        except:
            func =""

    return render_to_response('registrar.html',{
        'campos': campos,
        'func' : func,
        })




def registro(request):    
    usuario = request.POST["escolhido"]
    est = Estagiario.objects.get(pk=usuario)    
    #Se o usuário não tem nenhuma entrada em aberto naquele dia:
    if RegistroPonto.objects.filter(Estagiario= est, Data = datetime.now(), Saida=None).count() == 0:
        novoreg = RegistroPonto(Estagiario=est, Data=datetime.now(), Entrada=datetime.time(datetime.now()))
        novoreg.save()
        estado = 1
    #Se o usuário ja possui uma entrada naquele dia:
    else:
        def tolerancia(Hora, Fixo):
            fixodelta=timedelta(minutes=Fixo.minute,hours=Fixo.hour)
            horadelta=timedelta(minutes=Hora.minute,hours=Hora.hour)
            hmax = fixodelta + timedelta(minutes=15)
            hmin = fixodelta - timedelta(minutes=15)    
            if horadelta > hmax:
                    return 0
            elif horadelta < hmin:
                    return 0
            else:
                    return 1

        reg = RegistroPonto.objects.get(Estagiario= est, Data = datetime.now(), Saida=None)
        reg.Saida = datetime.time(datetime.now())
        reg.save()
        #Se o horário está dentro do Horário Fixo então ele é automaticamente aceito.
        for fix in HorarioFixo.objects.filter(Estagiario = est, DiaSemana=((datetime.now().weekday()+2) % 7)):
            if tolerancia(reg.Entrada,fix.Entrada) == 1:
                if tolerancia(reg.Saida, fix.Saida) ==1:
                    reg.Entrada = fix.Entrada
                    reg.Saida = fix.Saida
                    reg.Aceito = True
                    reg.save()


        estado = 2

    return HttpResponseRedirect( ('/?est=%d&estado=%d') % (est.id,estado) )


@login_required
@csrf_protect
def relatorios(request):    
    rel_urls = (
        ('Horarios Fixos','./horariofixo/'),
        ('Horarios Registrados','./horariosfeitos/'),
#        ('Banco de Horas','./bancohoras/'),
#        ('Horarios Aceitados','./horariosaceitados/'),
#        ('Estagiarios por Data Inicial(ranking)','./ranking/'),
    )


    minhas_urls = urls_type(rel_urls)

    return render_to_response('relatorios.html',{
        'minhas_urls':minhas_urls,
        })

def ranking(request):
    rank = Ocupada.objects.all().order_by('DataInicial')

    for i in rank:
        i.DataInicial = i.DataInicial.strftime("%d/%m/%Y")

    return render_to_response('ranking.html',{
        'rank':rank,
        })

@login_required
def horarios(request):
    manha=0
    tarde=1
    noite=2
    dom=[{},{},{}]      #declarando os dias com os tres períodos para cada
    seg=[{},{},{}]
    ter=[{},{},{}]
    qua=[{},{},{}]  
    qui=[{},{},{}]
    sex=[{},{},{}]
    sab=[{},{},{}]
    semana=[dom,seg,ter,qua,qui,sex,sab]        #declarando a semana

    def horaf(hora):
        return "%2.2d:%2.2d" % (hora.hour, hora.minute)

    #Pegando as horas de cada estagiário para montar a saida HTML    
    for est in Estagiario.objects.filter(Ativo=True):
        for dia in range(1,8):
            hor = HorarioFixo.objects.filter(Estagiario=est, DiaSemana=dia)
            for i in hor:                
                if i.Entrada < time(12,0):
                    if i.Saida <= time(12,0):
                        semana[dia-1][manha][est.Estagiario] = horaf(i.Entrada) + "-" + horaf(i.Saida)
                    else:
                        semana[dia-1][manha][est.Estagiario] = horaf(i.Entrada) + "-" + horaf(time(12,0))
                        semana[dia-1][tarde][est.Estagiario] = horaf(time(12,0)) + "-" + horaf(i.Saida)                        
                elif i.Entrada < time(18,0):
                    if i.Saida <= time(18,0):
                        semana[dia-1][tarde][est.Estagiario] = horaf(i.Entrada) + "-" + horaf(i.Saida)
                    else:
                        semana[dia-1][tarde][est.Estagiario] = horaf(i.Entrada) + "-" + horaf(time(18,0))
                        semana[dia-1][noite][est.Estagiario] = horaf(time(18,0)) + "-" + horaf(i.Saida)
                else:
                        semana[dia-1][noite][est.Estagiario] = horaf(i.Entrada) + "-" + horaf(i.Saida)

    linhas = []
    colunas= []
    for est in Estagiario.objects.filter(Ativo=True):
        colunas.append(est.Estagiario.title()[0:est.Estagiario.find(' ')+2])

    linhas.append(colunas)
    colunas=[]

    for dia in range(0,7):
        for periodo in range(0,3):
            for est in Estagiario.objects.filter(Ativo=True):
                colunas.append(semana[dia][periodo].get(est.Estagiario))
            linhas.append(colunas)
            colunas=[]


    contdias=0
    nomedias=['dom','seg','ter','qua','qui','sex','sab']
    periodos=['manha','tarde','noite']
    per=0
    saidas=[]
    for i in linhas:
        saidas.append("<TR>")
        if contdias==0:
            saidas.append("<TD>Dia</TD><TD>Periodo</TD>")
            contdias=1
        else:
            if per==0:
                saidas.append("<TD rowspan=3>%s</TD>" % (nomedias[(contdias-1) % 7]))

            saidas.append("<TD>%s</TD>" % (periodos[per]))
            per +=1        
            if per>2:
                per=0
                contdias+=1                
        for j in i:
            if j != None:
                saidas.append("<TD>%s</TD>" % j)
            else:
                saidas.append("<TD>&nbsp;</TD>")
        saidas.append("</TR>")

    return render_to_response('horarios.html',{
            'saidas': saidas,                
            })   

@login_required
def horariosfiltro(request):
    if request.method == 'POST':
        form = HorariosFeitos(request.POST)
        if form.is_valid():
            inicio = form.cleaned_data['De']
            fim = form.cleaned_data['Ate']
            if request.user.is_superuser ==True:
                ests = form.cleaned_data['ests']
            else:
                ests = [u'%s' % Estagiario.objects.filter(Ativo=True,Usuario_ad=request.user)[0].id]    
            print ests            
            def horaf(hora):
                try:
                    resp = "%2.2d:%2.2d" % (hora.hour, hora.minute)
                except:
                    resp = ""
                return resp

            atual = inicio
            colunas = []
            totais = {}
            if ests.count('0'):
                ests.__delitem__(ests.index('0'))
            while atual <= fim:
                linhas = []
                linhas.append(atual.strftime("%d/%m/%Y"))
                pos = timedelta(0)
                neg = timedelta(0)                
                for e in ests:
                    if totais.has_key(e)==False:
                        totais[e] = timedelta(0)
                    est = Estagiario.objects.get(pk = e)
                    hor = RegistroPonto.objects.filter(Estagiario=est,Data=atual)
                    horarios = " "
                    hordia= timedelta(0)
                    for i in hor:
                        if i.Aceito:
                            horarios += "<font color=darkblue>" + horaf(i.Entrada) + "-" + horaf(i.Saida) + "</font> "
                        else:
                            if request.user.is_authenticated() and i.Saida:
                                horarios += ("<a href=# onclick=javascript:window.open('./%s/','pop','height=10,width=10,scrollbars=no,status=no,location=no,menubar=no,toolbar=no')><font color=darkred>" % i.id) + horaf(i.Entrada) + "-" + horaf(i.Saida) + "</font></a> "
                            else:
                                horarios += "<font color=darkred>"  + horaf(i.Entrada) + "-" + horaf(i.Saida) + "</font> "
                        if i.Entrada and i.Saida:
                            hordia = timedelta(hours=i.Saida.hour,minutes=i.Saida.minute) - timedelta(
                                hours=i.Entrada.hour,minutes=i.Entrada.minute)
                    else:
                        hordia = timedelta(0)
                        totais[e] = totais[e] + hordia
                    linhas.append(horarios)

                atual = atual + timedelta(days=1)
                colunas.append(linhas)

            linhas=["Totais:"]
            for e in ests:
                linhas.append(totais[e])
            colunas.append(linhas)

            estagiarios = []
            for e in ests:
                estagiarios.append(str(Estagiario.objects.get(pk=e).Estagiario))

            return render_to_response ('filtradofeitos.html',{
                    'estagiarios': estagiarios,
                    'colunas': colunas,
                    })

    else:
        form = HorariosFeitos()
        return render_to_response('filtro.html' ,locals())

def acceptid(request, hor_id):
    hor = RegistroPonto.objects.get(pk = hor_id)
    if hor.Saida:
        hor.Aceito = True
        hor.save()
    return render_to_response('atuhor.html',{})

@login_required
def bancohoras(request):
    nomedias=['seg','ter','qua','qui','sex','sab','dom']
    saidaests = []
    saidabanco = []
    for est in Estagiario.objects.filter(Ativo=True):
        try:
            banco_horas = BancoHoras.objects.filter(Estagiario = est)[:1][0]
        except:
            continue
        ultimo_calculo = banco_horas.Data
        total = banco_horas.Total
        data = ultimo_calculo
        fim = datetime.now()
        neg = timedelta(0)  
        pos = timedelta(0)
        flag_aceito = True
        while data.date() < fim.date():
            #faz o calculo

            for fix in HorarioFixo.objects.filter(Estagiario = est, DiaSemana=((data.weekday()+2) % 7)): #Pegando os HorariosFixos daquele dia
                ent = timedelta(hours=fix.Entrada.hour,minutes = fix.Entrada.minute)
                sai = timedelta(hours=fix.Saida.hour, minutes=fix.Entrada.minute)
                if Feriado.objects.filter(Data=data.date()).count() == 0:
                    neg += sai - ent

            for hor in RegistroPonto.objects.filter(Estagiario = est, Data=data.date(), Aceito=True): #Pegando os Horarios Registrados daquele dia
                ent = timedelta(hours=hor.Entrada.hour,minutes = hor.Entrada.minute)
                sai = timedelta(hours=hor.Saida.hour, minutes=hor.Entrada.minute)
                pos += sai - ent
                if hor.Aceito==False:
                    flag_aceito = False

            data = data + timedelta(days=1)

        saidaests.append(est.Estagiario.title())
        saidabanco.append(total + Decimal(str(((pos.seconds / 3600.0) + (pos.days * 24.0)) - ((neg.seconds / 3600.0) + (neg.days * 24.0)))))
        if flag_aceito==True:
            banco_horas.Total = total + Decimal(str(((pos.seconds / 3600.0) + (pos.days * 24.0)) - ((neg.seconds / 3600.0) + (neg.days * 24.0))))
            banco_horas.Data = datetime.now()
            banco_horas.save()
        flag_aceito = True

    saida = estbank_type(saidaests,saidabanco)
    return render_to_response ('bancohoras.html',{
           'dados': saida,
           })
