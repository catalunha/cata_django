from django.db import models
from datetime import date,timedelta,datetime,timezone,time

from painel.models import User,Variavel
from painel.mixins import TimedModelMixin, UUIDModelMixin, UserModelMixin

from instituicao.models import Conhecimento
from tarefa.models import Avaliacao,Questao,Aplicada,Solucao,Relatorio,Anexo,Algoritmo,Codigo,Aplicada,Aplicado

# from django_markdown_ref.django_markdown_ref import DjangoMarkdownRef
# ref = DjangoMarkdownRef()
# ref.model = Variavel


from django_markdown_ref import DjangoMarkdownRef
ref = DjangoMarkdownRef()
ref.model = Variavel


import markdown
opcoes_mark = ["markdown.extensions.extra","markdown.extensions.abbr","markdown.extensions.attr_list","markdown.extensions.def_list","markdown.extensions.fenced_code","markdown.extensions.footnotes","markdown.extensions.tables","markdown.extensions.smart_strong","markdown.extensions.admonition","markdown.extensions.codehilite","markdown.extensions.headerid","markdown.extensions.meta","markdown.extensions.nl2br","markdown.extensions.sane_lists","markdown.extensions.smarty","markdown.extensions.toc","markdown.extensions.wikilinks","mdx_math",ref]

class Ementa(UUIDModelMixin, TimedModelMixin):
    conhecimento = models.ForeignKey(Conhecimento,related_name="ementas",on_delete = models.CASCADE)
    texto = models.TextField("Texto",blank=True,default=None, null=True, help_text='...')

    def __str__(self):
        return "{}".format(self.conhecimento)

    @property
    def texto_md(self):
        #markdown.markdown(some_text, extensions=[MyExtension(), 'path.to.my.ext', 'markdown.extensions.footnotes'])
        return markdown.markdown(self.texto, extensions=opcoes_mark)

    class Meta:
        verbose_name = "Ementa"
        verbose_name_plural = "Ementas"




class QuestaoStatus(UUIDModelMixin, TimedModelMixin):
    '''
    Descrição:
        Classe para analisar o status de uma questão do usuario
    Utilização:

    Parâmetros:
    iniciou
        Defini o inicio de desenvolvimento, abertura, de uma questão
    temporestante
        Defini o tempo restante para desenvolver a questão
    '''

    aplicada = models.ForeignKey(Aplicada,related_name="status",on_delete = models.CASCADE)

    iniciou = models.DateTimeField('DataHora Início',default=None,null=True,blank=True,help_text='...')
    tempo = models.TimeField('Tempo',default=None,null=True,blank=True,help_text='...')
    tentativa = models.PositiveSmallIntegerField('Tentativa',default=0,null=True,blank=True,help_text='...')
    ativo = models.BooleanField("Ativa",default = True,help_text='...')

    def __str__(self):
        return '{}'.format(self.aplicada)

    class Meta:
        #unique_together = ("aplicada")
        ordering = ["aplicada__usuario__last_name"]
        verbose_name = "Status da Questão"
        verbose_name_plural = "Status da Questões"

    def tentou(self):
        if self.tentativa is not None :
            self.tentativa=self.tentativa+1
            self.save()

    def save(self, *args, **kwargs):
        # # print('+++ diario->models.py->QuestaoStatus +++')

        #questao_tempo=Questao.objects.get(id=self.questao.id).tempo
        questao_tempo=self.aplicada.questao.tempo
        #questao_tentativa=Questao.objects.get(id=self.questao.id).tentativa
        questao_tentativa=self.aplicada.questao.tentativa
        avaliacao_fim=self.aplicada.questao.avaliacao.fim
        # print('1: {} {} {} {} {}'.format(questao_tempo,questao_tentativa,avaliacao_fim,self.iniciou,self.aplicada.id))

        if self.iniciou is None:
            self.ativo = True
            self.tempo = questao_tempo
            self.tentativa = 0
        if questao_tempo and self.iniciou is not None:
            # # print('======>')
            dhi_dt=self.iniciou
            questao_tempo_td=timedelta(hours=questao_tempo.hour,minutes=questao_tempo.minute)
            dhf_dt=dhi_dt+questao_tempo_td
            if dhf_dt > avaliacao_fim:
                dhf_dt = avaliacao_fim
            agora_dt=datetime.now(timezone.utc)
            restante_td=dhf_dt-agora_dt
            restante_b=restante_td.total_seconds() > 0 and restante_td<questao_tempo_td
            if restante_b:
                h=int(restante_td.seconds/3600.0+restante_td.days*24)
                m=int(restante_td.seconds%3600.0/60.0)
                self.tempo = time(h,m)
                self.ativo = True
            else:
                self.tempo = time(0,0)
                self.ativo = False
        if questao_tentativa and self.tentativa >= questao_tentativa:
            self.ativo = False
        # print('--- diario->models.py->QuestaoStatus ---')
        super(QuestaoStatus, self).save(*args, **kwargs)


class AlgoritmoStatus(UUIDModelMixin, TimedModelMixin):
    '''
    Descrição:
        Classe para analisar o status de uma questão do usuario
    Utilização:

    Parâmetros:
    iniciou
        Defini o inicio de desenvolvimento, abertura, de uma questão
    temporestante
        Defini o tempo restante para desenvolver a questão
    '''

    aplicado = models.ForeignKey(Aplicado,related_name="status_aplicado",on_delete = models.CASCADE)

    iniciou = models.DateTimeField('DataHora Início',default=None,null=True,blank=True,help_text='...')
    tempo = models.TimeField('Tempo',default=None,null=True,blank=True,help_text='...')
    ativo = models.BooleanField("Ativa",default = True,help_text='...')

    def __str__(self):
        return '{}'.format(self.aplicado)

    class Meta:
        #unique_together = ("aplicado")
        ordering = ["aplicado__usuario__last_name"]
        verbose_name = "Status do Algoritmo"
        verbose_name_plural = "Status do Algoritmo"

    def save(self, *args, **kwargs):
        # print('+++ diario->models.py->AlgoritmoStatus +++')

        algoritmo_tempo=self.aplicado.algoritmo.tempo
        avaliacao_fim=self.aplicado.algoritmo.avaliacao.fim
        # print('1: {} {} {} {}'.format(algoritmo_tempo,avaliacao_fim,self.iniciou,self.aplicado.id))

        if self.iniciou is None:
            self.ativo = True
            self.tempo = algoritmo_tempo
        if algoritmo_tempo and self.iniciou is not None:
            # print('======>')
            dhi_dt=self.iniciou
            algoritmo_tempo_td=timedelta(hours=algoritmo_tempo.hour,minutes=algoritmo_tempo.minute)
            dhf_dt=dhi_dt+algoritmo_tempo_td
            if dhf_dt > avaliacao_fim:
                dhf_dt = avaliacao_fim
            agora_dt=datetime.now(timezone.utc)
            restante_td=dhf_dt-agora_dt
            restante_b=restante_td.total_seconds() > 0 and restante_td<algoritmo_tempo_td
            if restante_b:
                h=int(restante_td.seconds/3600.0+restante_td.days*24)
                m=int(restante_td.seconds%3600.0/60.0)
                self.tempo = time(h,m)
                self.ativo = True
            else:
                self.tempo = time(0,0)
                self.ativo = False
        # print('--- diario->models.py->AlgoritmoStatus ---')
        super(AlgoritmoStatus, self).save(*args, **kwargs)
