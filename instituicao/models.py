from django.db import models
from django.contrib import admin
from django.contrib.admin import AdminSite
from datetime import date,time,datetime,timedelta
from django.utils import timezone

from painel.models import User
from painel.mixins import TimedModelMixin, UUIDModelMixin, UserModelMixin

class Instituicao(UUIDModelMixin, TimedModelMixin):
    nome = models.CharField(verbose_name="Nome", max_length = 255)

    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True, default=None)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

    def __str__(self):
        return "{}".format(self.nome)

class Conhecimento(UUIDModelMixin, TimedModelMixin, UserModelMixin):
    nome = models.CharField(verbose_name="Nome",max_length = 255,help_text='...')
    instituicao = models.ForeignKey(Instituicao,related_name="conhecimentos",on_delete = models.CASCADE,help_text='...')

    ativo = models.BooleanField(default = True,help_text='...')
    descricao = models.TextField(verbose_name="Descrição",blank=True,null=True,default=None,help_text='...')
    inicio = models.DateTimeField('Data de Início',default=timezone.now,null=True,blank=True,help_text='...')
    fim = models.DateTimeField('Data de Fim',default=timezone.now,null=True,blank=True,help_text='...')

    def __str__(self):
        return "{} > {}".format(self.usuario.last_name,self.nome)

    class Meta:
        unique_together = ("instituicao", "nome")
        ordering = ["nome"]
        verbose_name = "Conhecimento"
        verbose_name_plural = "Conhecimentos"

class Turma(UUIDModelMixin, TimedModelMixin):
    nome = models.CharField("Nome",max_length = 255)
    conhecimento = models.ForeignKey(Conhecimento,related_name="turmas",on_delete = models.CASCADE)
    alunos = models.ManyToManyField(User,related_name="na_turma",limit_choices_to={'cargo':'aluno'},blank=True,help_text='...')

    ativo = models.BooleanField("Ativo",default = True,help_text='...')
    descricao = models.TextField("Descrição",blank=True,null=True,default=None)
    inicio = models.DateTimeField('Data de Início',default=timezone.now,null=True,blank=True,help_text='...')
    fim = models.DateTimeField('Data de Fim',default=datetime.now,null=True,blank=True,help_text='...')

    questao = models.IntegerField(editable=False,default=0)

    def alunos_mm(self):
        return " ".join(['*{}-{}'.format(p.last_name,p.username) for p in self.alunos.all().order_by('last_name')])

    def __str__(self):
        return "{} > {}".format(self.conhecimento.nome,self.nome)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
