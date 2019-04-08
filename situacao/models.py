from django.db import models

from painel.mixins import TimedModelMixin, UUIDModelMixin, UserModelMixin
from painel.models import User
from instituicao.models import Conhecimento,Turma

class Indice(UUIDModelMixin, TimedModelMixin):
    conhecimento = models.ForeignKey(Conhecimento,related_name="indices",on_delete = models.CASCADE)
    nome = models.CharField("Nome",max_length = 255)
    ordem = models.PositiveSmallIntegerField(blank = True)

    superior = models.ForeignKey('self', on_delete = models.CASCADE,blank=True,null = True,related_name="subindices")
    descricao = models.TextField("Descrição",blank=True,null=True,default=None)

    class Meta:
        ordering = ["ordem","superior__nome", "nome"]
        verbose_name = "Indice"
        verbose_name_plural = "Indices"

    def __concat_str__(self):
        if self.superior is None:
            return self.nome
        else:
            return self.superior.__concat_str__() + ' -> ' + self.nome

    def __str__(self):
        return self.__concat_str__()


    def save(self, *args, **kwargs):
        if self.ordem is None:
            self.ordem = self.proxima_ordem()
        super(Indice, self).save(*args, **kwargs)

    def proxima_ordem(self):
        b = Indice.objects.all().order_by("-ordem").first()
        ## print(b)
        if b is None:
            return 0
        else:
            return b.ordem + 1

    def subir_ordem(self):
        if self == Indice.objects.filter(superior=None).first() or self == Indice.objects.filter(superior=self.superior).first():
            #raise OrdemException("Indice nao pode subir")
            return 0
        if self.superior is None:
            irmaos = Indice.objects.filter(superior=None)
        else:
            irmaos = Indice.objects.filter(superior=self.superior)
        irmaos = list(irmaos)
        irmao = irmaos[irmaos.index(self)-1]
        self.ordem, irmao.ordem = irmao.ordem, self.ordem
        self.save()
        irmao.save()

    def descer_ordem(self):
        if self == Indice.objects.filter(superior=None).last() or self == Indice.objects.filter(superior=self.superior).last():
            #raise OrdemException("Indice nao pode descer")
            return 0
        if self.superior is None:
            irmaos = Indice.objects.filter(superior=None)
        else:
            irmaos = Indice.objects.filter(superior=self.superior)
        irmaos = list(irmaos)
        irmao = irmaos[irmaos.index(self)+1]
        self.ordem, irmao.ordem = irmao.ordem, self.ordem
        self.save()
        irmao.save()

    def get_arvore_genealogica(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in self.subindices.all():
            _r = c.get_arvore_genealogica(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r



def problema_pdf(instance, filename):
    return "situacao/problema/pdf/{}_{}".format(instance.id, filename)

class Problema(UUIDModelMixin, TimedModelMixin):
    usuario = models.ForeignKey(User, related_name="problemas", on_delete = models.CASCADE)
    referencia  = models.CharField("Referência",max_length=255,help_text='...')
    descricao  = models.CharField("Descrição",max_length=255,help_text='...')
    pdf=models.FileField('PDF:',upload_to=problema_pdf,max_length=2555,help_text='Anexar somente arquivos com o pdf da situação.')
    proposta  = models.TextField("Proposta",help_text='A proposta pode ser em texto, markdown ou latex.',null=True,blank=True,default=None, )
    solucao  = models.TextField("Solução",help_text='...',null=True,blank=True,default=None, )
    observacao  = models.TextField("Observação",help_text='...',null=True,blank=True,default=None, )
    uso = models.PositiveSmallIntegerField('Uso',null=True,blank=True,help_text='...')
    usos  = models.CharField("Usos",max_length=2550,null=True,blank=True,help_text='...')

    ativo = models.BooleanField("Ativo",default = True,help_text='...')
    indices = models.ManyToManyField(Indice,related_name="no_problema",help_text='Ligado a que índices:',)
    def __str__(self):
        return '{} > {}.'.format(self.referencia,self.descricao)

    def indices_mm(self):
        return " ".join(['*{} '.format(p.__concat_str__()) for p in self.indices.all().order_by('nome')])

    def get_usos(self):
        lista=[]
        totalgeral=0
        for turma in Turma.objects.filter(conhecimento__usuario=self.usuario,ativo=True):
            total=0
            for avaliacao in turma.avaliacoes.all():
                for questao in avaliacao.questoes.all():
                    if questao.problema.id==self.id :
                        total = total + 1
                        totalgeral = totalgeral + 1
            if total > 0 :
                lista.append('{}: {}'.format(turma,total))
        self.uso=totalgeral
        self.usos='; '.join(lista)
        self.save()

    class Meta:
        unique_together = ("usuario", "referencia")
        ordering = ["referencia"]
        verbose_name = "Problema"
        verbose_name_plural = "Problemas"

class Simulacao(UUIDModelMixin, TimedModelMixin):
    problema = models.ForeignKey(Problema,related_name="simulacoes",on_delete = models.CASCADE,help_text='...')

    def __str__(self):
        return 'SimulacaoID={}:{}'.format(self.id,self.problema)

    class Meta:
        ordering = ["id", 'problema']
        verbose_name = "Simulação"
        verbose_name_plural = "Simulações"

class ValorAleatorio(UUIDModelMixin, TimedModelMixin):
    simulacao = models.ForeignKey(Simulacao,related_name="valores_aleatorios",on_delete = models.CASCADE,help_text='...')

    nome = models.CharField('Nome',max_length=25,help_text='...')
    valor = models.CharField('Valor',max_length=25,help_text='...')

    def __str__(self):
        return 'idVA={}:{}:{}'.format(self.id,self.simulacao,self.nome)

    class Meta:
        unique_together = ("simulacao", "nome")
        ordering = ["simulacao", 'nome']
        verbose_name = "Valor Aleatorio"
        verbose_name_plural = "Valores Aleatorios"

class Resposta(UUIDModelMixin, TimedModelMixin):
    simulacao = models.ForeignKey(Simulacao,related_name="respostas",on_delete = models.CASCADE,help_text='...')
    letra = models.CharField('Letra',max_length=5,help_text='...')

    valor = models.CharField('Valor',max_length=55,help_text='...')

    def __str__(self):
        return 'idResp={}:{}:{}'.format(self.id,self.simulacao,self.letra)

    class Meta:
        unique_together = ("simulacao", "letra")
        ordering = ["simulacao", 'letra']
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"

class Texto(UUIDModelMixin, TimedModelMixin):
    simulacao = models.ForeignKey(Simulacao,related_name="textos",on_delete = models.CASCADE,help_text='...')
    letra = models.CharField('Letra',max_length=5,help_text='...')

    texto = models.TextField('Texto:',null=True,blank=True,default=None,help_text='...')

    def __str__(self):
        return 'idTxt={}:{}:{}'.format(self.id,self.simulacao,self.letra)

    class Meta:
        unique_together = ("simulacao", "letra")
        ordering = ["simulacao", 'letra']
        verbose_name = "Texto"
        verbose_name_plural = "Textos"

def arquivo_questao(instance, filename):
    return "situacao/arquivo/arquivo/{0}_{1}".format(instance.id, filename)

class Arquivo(UUIDModelMixin, TimedModelMixin):
    simulacao = models.ForeignKey(Simulacao,related_name="arquivos",on_delete = models.CASCADE,help_text='...')
    letra = models.CharField('Letra',max_length=5,help_text='...')

    arquivo = models.FileField('Arquivo:',upload_to=arquivo_questao,null=True,blank=True,default=None,help_text='...')

    def __str__(self):
        return 'idArq={}:{}:{}'.format(self.id,self.simulacao,self.letra)

    class Meta:
        unique_together = ("simulacao", "letra")
        ordering = ["simulacao", 'letra']
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

def programa_pdf(instance, filename):
    return "situacao/programa/pdf/{0}_{1}".format(instance.id, filename)

class Programa(UUIDModelMixin, TimedModelMixin):
    usuario = models.ForeignKey(User, related_name="programas", on_delete = models.CASCADE)
    referencia  = models.CharField("Referência",max_length=255,help_text='...',unique=True)
    descricao  = models.CharField("Descrição",max_length=255,help_text='...')
    pdf=models.FileField('PDF:',upload_to=programa_pdf,help_text='Anexar somente arquivos com o pdf da situação.')

    indices = models.ManyToManyField(Indice,related_name="nos_programas",help_text='Ligado a que índices:')
    ativo = models.BooleanField("Ativo",default = True)
    observacao  = models.TextField("Observação",max_length=255,help_text='...',null=True,blank=True,default=None,)
    uso = models.PositiveSmallIntegerField('Uso',null=True,blank=True,help_text='...')
    usos  = models.CharField("Usos",max_length=2550,null=True,blank=True,help_text='...')

    def __str__(self):
        return '{} > {}.'.format(self.referencia,self.descricao)

    def indices_mm(self):
        return " ".join(['*{}\n'.format(p.nome) for p in self.indices.all().order_by('nome')])

    def get_usos(self):
        lista=[]
        totalgeral=0
        for turma in Turma.objects.filter(conhecimento__usuario=self.usuario,ativo=True):
            total=0
            for avaliacao in turma.avaliacoes.all():
                for algoritmo in avaliacao.algoritmos.all():
                    if algoritmo.programa.id==self.id :
                        total = total + 1
                        totalgeral = totalgeral + 1
            if total > 0 :
                lista.append('{}: {}'.format(turma,total))
        self.uso=totalgeral
        self.usos='; '.join(lista)
        self.save()

    class Meta:
        ordering = ["referencia"]
        verbose_name = "Programa"
        verbose_name_plural = "Programas"


class Proposta(UUIDModelMixin, TimedModelMixin):
    TIPO=(('interface.py','interface.py'),('solucao.py','solucao.py'),('entrada.txt','entrada.txt'),('dados.txt','dados.txt'),)

    programa = models.ForeignKey(Programa,related_name="propostas",on_delete = models.CASCADE)
    arquivo = models.CharField('Arquivo',max_length=25,choices=TIPO)
    conteudo = models.TextField('Conteúdo do arquivo',blank=True,default=None,null=True,help_text='...')

    ativo = models.BooleanField("Ativa",default = True,help_text='...')

    def __str__(self):
        return '{}'.format(self.programa)

    class Meta:
        unique_together = ("programa", "arquivo")
        verbose_name = "Proposta"
        verbose_name_plural = "Propostas"


class Teste(UUIDModelMixin, TimedModelMixin):
    programa = models.ForeignKey(Programa,related_name="testes",on_delete = models.CASCADE)

    entrada = models.TextField(max_length=2555,blank=True,null=True,default=None,help_text='...')
    saida = models.TextField(max_length=2555,blank=True,null=True,default=None,help_text='...')

    def __str__(self):
        return 'idTst={}:{}'.format(self.id,self.programa)

    class Meta:
        ordering = ["programa"]
        verbose_name = "Teste"
        verbose_name_plural = "Testes"
