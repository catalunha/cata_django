from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

from painel.mixins import TimedModelMixin, UUIDModelMixin, UserModelMixin

class User(AbstractUser, UUIDModelMixin):
    CARGO=(('professor','Professor(a)'),('aluno','Aluno(a)'),('admin','Administrador(a)'),)

    # cargo
    cargo = models.CharField('Cargo',max_length=25,choices=CARGO)
    professor = models.ManyToManyField('self',symmetrical=False,related_name="professores",blank=True,default=None)

    objects = UserManager()

    class Meta:
        ordering = ["last_name"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def professores_mm(self):
        return " ".join(['*{} '.format(p.last_name) for p in self.professor.all()])

    def __concat_str__(self):
        if not self.professor.all():
            return self.last_name
        else:
            return self.professores_mm() + ' :-) ' + self.last_name

    def __str__(self):
        return self.__concat_str__()
        #return self.last_name



def variavel_arquivo(instance, filename):
    return "painel/variavel/arquivo/{}_{}".format(instance.id, filename)

class Variavel(UUIDModelMixin, TimedModelMixin, UserModelMixin):
    nome = models.CharField("Nome",max_length=100,help_text='Sem espaços, nem acentos. Tudo minúsculo.')
    valor = models.CharField("Valor",max_length=255,blank=True,default=None,null=True,help_text='...')
    texto = models.TextField("Texto",blank=True,default=None, null=True, help_text='...')
    arquivo = models.FileField("Arquivo",blank = True, default=None, null=True, upload_to = variavel_arquivo)

    class Meta:
        unique_together = ("usuario", "nome")
        verbose_name = "Variável"
        verbose_name_plural = "Variáveis"

    def __str__(self):
        return "{}".format(self.nome)

    def get_url(self):
        if self.arquivo is not None:
            return self.arquivo.url
        else:
            return "/arquivosemcaminho/"
