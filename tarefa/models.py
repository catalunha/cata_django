from django.db import models
from django.conf import settings
import datetime


from painel.mixins import TimedModelMixin, UUIDModelMixin, UserModelMixin
from painel.models import User

from instituicao.models import Turma
from situacao.models import Problema,Simulacao,Programa,Resposta,Arquivo,Texto,Proposta


class Avaliacao(UUIDModelMixin, TimedModelMixin):
    turma = models.ForeignKey(Turma,related_name="avaliacoes",on_delete = models.CASCADE)
    nome = models.CharField(max_length = 255)
    inicio = models.DateTimeField('Data Início',help_text='...')
    fim = models.DateTimeField('Data Fim',help_text='...')

    privada = models.BooleanField(default = True)
    ativo = models.BooleanField("Ativa",default = True,help_text='...')
    nota = models.PositiveSmallIntegerField('Nota',default=1,help_text='...')

    def __str__(self):
        return '{} > {}.'.format(self.turma,self.nome)

    class Meta:
        unique_together = ("turma", "nome")
        ordering = ["turma", "nome","inicio"]
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

class Questao(UUIDModelMixin, TimedModelMixin):
    avaliacao = models.ForeignKey(Avaliacao,related_name="questoes",related_query_name="campo_avaliacao",on_delete = models.CASCADE)
    problema = models.ForeignKey(Problema,related_name="na_questao",on_delete = models.CASCADE)

    ativo = models.BooleanField("Ativa",default=True,help_text='...')
    tentativa = models.PositiveSmallIntegerField('Tentativa',default=3,null=True,blank=True,help_text='...')
    tempo = models.TimeField("Tempo",default=datetime.time(2, 00),null=True,blank=True,help_text='...')# Pode ser None por causa dos projetos. Até fechar avaliacao
    nota = models.PositiveSmallIntegerField('Nota',default=1,help_text='...')

    numero = models.IntegerField("Numero",editable=False)

    def __str__(self):
        return '{} > {} > {}.'.format(self.avaliacao,self.problema,self.numero)

    class Meta:
        ordering = ["avaliacao__nome", "problema__referencia"]
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def save(self, *args, **kwargs):
        if self.numero is None:
            turma=Turma.objects.get(id=self.avaliacao.turma.id)
            turma.questao = turma.questao + 1
            turma.save()
            self.numero = turma.questao
        super(Questao, self).save(*args, **kwargs)

class Aplicada(UUIDModelMixin, TimedModelMixin):
    usuario = models.ForeignKey(User, related_name="aplicadas_usuario", on_delete = models.CASCADE)
    questao = models.ForeignKey(Questao,related_name="aplicadas",on_delete = models.CASCADE)

    ativo = models.BooleanField("Ativa",default = True,help_text='...')

    def __str__(self):
        return 'AplicadaID={}'.format(self.id)

    def get_total_solucao(self):
        total=0
        for solucao in Solucao.objects.filter(aplicada=self.id) :
            if solucao.nota :
                total += solucao.nota
        return total*self.questao.nota*self.questao.avaliacao.nota

    def get_total_relatorio(self):
        total=0
        for relatorio in Relatorio.objects.filter(aplicada=self.id) :
            if relatorio.nota :
                total += relatorio.nota
        return total*self.questao.nota*self.questao.avaliacao.nota

    def get_total_anexo(self):
        total=0
        for anexo in Anexo.objects.filter(aplicada=self.id) :
            if anexo.nota :
                total += anexo.nota
        return total*self.questao.nota*self.questao.avaliacao.nota

    class Meta:
        unique_together = ("usuario","questao")
        ordering = ["questao__numero"]
        verbose_name = "Questao Aplicada"
        verbose_name_plural = "Questões Aplicadas"

class Solucao(UUIDModelMixin, TimedModelMixin):
    aplicada = models.ForeignKey(Aplicada,related_name="solucoes_aplicada",on_delete = models.CASCADE)
    resposta = models.ForeignKey(Resposta,related_name="solucoes_resposta",on_delete = models.CASCADE,help_text='...')

    ativo = models.BooleanField("Ativa",default = True,help_text='...')
    solucao = models.CharField('Valor',max_length=255,blank=True,default='',null=True,help_text='...')
    nota = models.PositiveSmallIntegerField('Nota',blank=True,default=None,null=True,help_text='...')

    def __str__(self):
        return 'SolucaoID={}'.format(self.id)

    class Meta:
        unique_together = ("aplicada","resposta")
        ordering = ["aplicada","resposta"]
        verbose_name = "Solução"
        verbose_name_plural = "Soluções"

class Relatorio(UUIDModelMixin, TimedModelMixin):
    aplicada = models.ForeignKey(Aplicada,related_name="relatorios_aplicada",on_delete = models.CASCADE)
    texto = models.ForeignKey(Texto,related_name="relatorios_texto",on_delete = models.CASCADE,help_text='...')

    relatorio = models.TextField('Relatório:',blank=True,default='',null=True,help_text='...')
    nota = models.PositiveSmallIntegerField('Nota',blank=True,default=None,null=True,help_text='...')
    ativo = models.BooleanField("Ativa",default = True,help_text='...')

    def __str__(self):
        return 'RelatorioID={}'.format(self.id)

    class Meta:
        unique_together = ("aplicada","texto")
        ordering = ["aplicada", "texto"]
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"

def arquivo_questao(instance, filename):
    return "tarefa/anexo/arquivo/{0}_{1}".format(instance.id, filename)

class Anexo(UUIDModelMixin, TimedModelMixin):
    aplicada = models.ForeignKey(Aplicada,related_name="anexos_aplicada",on_delete = models.CASCADE)
    arquivo = models.ForeignKey(Arquivo,related_name="anexos_arquivo",on_delete = models.CASCADE,help_text='...')

    anexo = models.FileField('Arquivo:',upload_to=arquivo_questao,max_length=255,default=None,blank=True,help_text='...')
    nota = models.PositiveSmallIntegerField('Nota',blank=True,default=None,null=True,help_text='...')
    ativo = models.BooleanField("Ativa",default = True,help_text='...')

    def __str__(self):
        return 'Anexo={}'.format(self.id)

    class Meta:
        unique_together = ("aplicada","arquivo")
        ordering = ["aplicada", "arquivo"]
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"

#Algoritmo é o mesmo que questão
class Algoritmo(UUIDModelMixin, TimedModelMixin):
    avaliacao = models.ForeignKey(Avaliacao,related_name="algoritmos",on_delete = models.CASCADE)
    programa = models.ForeignKey(Programa,related_name="no_algoritmo",on_delete = models.CASCADE)

    ativo = models.BooleanField("Ativo",default = True,help_text='...')
    tempo = models.TimeField("Tempo",default=datetime.time(2, 00),null=True,blank=True,help_text='...')# Pode ser None por causa dos projetos. Até fechar avaliacao
    nota = models.PositiveSmallIntegerField('Nota',default=1,help_text='...')

    numero = models.IntegerField("Numero",editable=False)

    def __str__(self):
        return 'idAlg={}:{}'.format(self.id,self.numero)

    class Meta:
        ordering = ["avaliacao__nome", "programa__referencia"]
        verbose_name = "Algoritmo"
        verbose_name_plural = "Algoritmos"

    def save(self, *args, **kwargs):
        if self.numero is None:
            turma=Turma.objects.get(id=self.avaliacao.turma.id)
            turma.questao = turma.questao + 1
            turma.save()
            self.numero = turma.questao
        super(Algoritmo, self).save(*args, **kwargs)


#Algoritmo aplicado é o mesmo que questão aplicada
class Aplicado(UUIDModelMixin, TimedModelMixin):
    usuario = models.ForeignKey(User, related_name="aplicados_usuario", on_delete = models.CASCADE)
    algoritmo = models.ForeignKey(Algoritmo,related_name="aplicados",on_delete = models.CASCADE)

    ativo = models.BooleanField("Ativa",default = True,help_text='...')

    def __str__(self):
        return 'idApldo={}'.format(self.id)

    class Meta:
        unique_together = ("usuario","algoritmo")
        ordering = ["algoritmo__numero"]
        verbose_name = "Algoritmo Aplicado"
        verbose_name_plural = "Algoritmos Aplicados"

    def get_total_codigo(self):
        total=0
        for codigo in Codigo.objects.filter(aplicado=self.id) :
            if codigo.nota :
                total += codigo.nota
        return total*self.algoritmo.nota*self.algoritmo.avaliacao.nota



def arquivo_algoritmo(instance, filename):
    return "tarefa/AlgoritmoArquivo/{0}_{1}".format(instance.id, filename)

# Codigo é o mesmo que solucao ou relatorio ou anexo
class Codigo(UUIDModelMixin, TimedModelMixin):
    aplicado = models.ForeignKey(Aplicado,related_name="codigos_aplicado",on_delete = models.CASCADE)
    proposta = models.ForeignKey(Proposta,related_name="codigos_proposta",on_delete = models.CASCADE,help_text='...')

    conteudo = models.TextField('Conteúdo do arquivo',blank=True,default='',null=True,help_text='...')
    nota = models.PositiveSmallIntegerField('Nota',blank=True,default=None,null=True,help_text='...')
    ativo = models.BooleanField("Ativa",default = True,help_text='...')

    def __str__(self):
        return 'idCod={}'.format(self.id)

    class Meta:
        unique_together = ("aplicado", "proposta")
        verbose_name = "Codigo"
        verbose_name_plural = "Codigos"
