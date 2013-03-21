# -*- coding: utf-8 -*-
from django.db import models

class Unidade(models.Model):
    Unidade = models.CharField(max_length=80, unique=True)
    def __unicode__(self):
        return self.Unidade

class Curso(models.Model):
    Unidade = models.ForeignKey(Unidade)
    Curso = models.CharField(max_length=200)
    def __unicode__(self):
        return self.Curso

class Estagiario(models.Model):
    class Meta:
        ordering = ('Estagiario',)
    NUSP = models.IntegerField(unique=True)
    Estagiario = models.CharField(max_length=200)
    Unidade = models.ForeignKey(Unidade)
    Curso = models.ForeignKey(Curso)
    Ingresso = models.DateField(null=True,blank=True)
    CPF = models.CharField(max_length=200)
    RG = models.CharField(max_length=200)
    Email = models.EmailField()
    Ag = models.CharField("Agencia",max_length=6)
    Conta = models.CharField(max_length=11)
    Banco = models.CharField(max_length=200,default = 'Nossa Caixa')
    Ativo = models.BooleanField(default=1)
    Foto = models.ImageField(upload_to='fotos/',null=True,blank=True)
    Impressao = models.TextField()
    Usuario_ad = models.CharField('Conta do AD',max_length=200)
    def __unicode__(self):
        return self.Estagiario

class Celular(models.Model):
    Estagiario = models.ForeignKey(Estagiario)
    DDD = models.PositiveSmallIntegerField()
    Celular = models.IntegerField()
    def __unicode__(self):
        return str(self.Celular)

class Estado(models.Model):
    Estado = models.CharField(max_length=2,unique=True)
    def __unicode__(self):
        return self.Estado

class Endereco(models.Model):
    Estagiario = models.ForeignKey(Estagiario)
    Logradouro = models.CharField(max_length=200)
    Numero = models.IntegerField(null=True,blank=True)
    Complemento = models.CharField(max_length=50,null=True,blank=True)
    Bairro = models.CharField(max_length=200)
    CEP = models.CharField(max_length=9)
    DDD = models.PositiveSmallIntegerField(null=True,blank=True)
    Telefone= models.IntegerField(null=True,blank=True)
    Cidade = models.CharField(max_length=200)
    Estado = models.ForeignKey(Estado)
    def __unicode__(self):
        return self.Logradouro

class Tipo_Vaga(models.Model):
    Tipo_Vaga = models.CharField(max_length=200)
    Horas = models.PositiveSmallIntegerField()
    Bolsa = models.FloatField()
    class Meta:
        verbose_name = "Tipo de Vaga"
        verbose_name_plural = "Tipos de Vagas"
    def __unicode__(self):
        return self.Tipo_Vaga
    
class Vaga(models.Model):
    Tipo_Vaga = models.ForeignKey(Tipo_Vaga)
    Vaga = models.CharField(max_length=200)
    DataInicial = models.DateField(null=True, blank=True)
    DataFinal = models.DateField(null=True,blank=True)
    def __unicode__(self):
        return self.Vaga

class Ocupada(models.Model):
    Vaga = models.ForeignKey(Vaga)
    Estagiario = models.ForeignKey(Estagiario)
    DataInicial = models.DateField(null=True, blank=True)
    DataFinal = models.DateField(null=True,blank=True)
    class Meta:
        verbose_name = "Vaga Ocupada"
        verbose_name_plural = "Vagas Ocupadas"
    def __unicode__(self):
        return str(self.Vaga) + " : " + str(self.Estagiario)

class HorarioFixo(models.Model):
    Estagiario = models.ForeignKey(Estagiario)    
    Dia_Semana = (
        (1,'Domingo'),
        (2,'Segunda-feira'),
        (3,'Terca-feira'),
        (4,'Quarta-feira'),
        (5,'Quinta-feira'),
        (6,'Sexta-feira'),
        (7,'Sabado')
        )
    DiaSemana = models.IntegerField(choices=Dia_Semana)
    Entrada = models.TimeField()
    Saida = models.TimeField()
    def __unicode__(self):          
        return self.Dia_Semana[self.DiaSemana-1][1] + ": " + str(self.Entrada) + " - " + str(self.Saida)

class RegistroPonto(models.Model):
    Estagiario = models.ForeignKey(Estagiario)
    Data = models.DateField()
    Entrada = models.TimeField()
    Saida = models.TimeField(null=True,blank=True) 
    Aceito = models.BooleanField()
    Pago = models.BooleanField()
    class Meta:
        ordering= ["-Data","Entrada"]
    def __unicode__(self):
        txtsaida = ("%s" % self.Entrada)[0:5]
        return unicode(txtsaida)

class Feriado(models.Model):
    Data = models.DateField()
    Obs = models.TextField(blank=True)
    def __unicode__(self):
        return unicode(self.Data)

class BancoHoras(models.Model):
    Estagiario = models.ForeignKey(Estagiario)
    #Data = models.DateTimeField(auto_now=True)
    Data = models.DateTimeField()
    Total = models.DecimalField(max_digits=5,decimal_places=1)
    class Meta:
        verbose_name= "Banco de Horas"
        verbose_name_plural = "Banco de Horas"
        #ordering = "-Data"
    def __unicode__(self):
        return str(self.Estagiario) + " : " + str(self.Total)
    
