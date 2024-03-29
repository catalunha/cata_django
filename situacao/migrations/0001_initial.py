# Generated by Django 2.0.4 on 2018-07-26 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import situacao.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instituicao', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('letra', models.CharField(help_text='...', max_length=5, verbose_name='Letra')),
                ('arquivo', models.FileField(blank=True, default=None, help_text='...', null=True, upload_to=situacao.models.arquivo_questao, verbose_name='Arquivo:')),
            ],
            options={
                'verbose_name': 'Arquivo',
                'verbose_name_plural': 'Arquivos',
                'ordering': ['simulacao', 'letra'],
            },
        ),
        migrations.CreateModel(
            name='Indice',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, default=None, null=True, verbose_name='Descrição')),
                ('conhecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indices', to='instituicao.Conhecimento')),
                ('superior', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='situacao.Indice')),
            ],
            options={
                'verbose_name': 'Indice',
                'verbose_name_plural': 'Indices',
                'ordering': ['superior__nome', 'nome'],
            },
        ),
        migrations.CreateModel(
            name='Problema',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('referencia', models.CharField(help_text='...', max_length=255, unique=True, verbose_name='Referência')),
                ('descricao', models.CharField(help_text='...', max_length=255, verbose_name='Descrição')),
                ('pdf', models.FileField(help_text='Anexar somente arquivos com o pdf da situação.', max_length=2555, upload_to=situacao.models.problema_pdf, verbose_name='PDF:')),
                ('ativo', models.BooleanField(default=True, help_text='...', verbose_name='Ativo')),
                ('observacao', models.TextField(blank=True, default=None, help_text='...', max_length=255, verbose_name='Observação')),
                ('indices', models.ManyToManyField(help_text='Ligado a que índices:', related_name='no_problema', to='situacao.Indice')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problemas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Problema',
                'verbose_name_plural': 'Problemas',
                'ordering': ['referencia'],
            },
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('referencia', models.CharField(help_text='...', max_length=255, unique=True, verbose_name='Referência')),
                ('descricao', models.CharField(help_text='...', max_length=255, verbose_name='Descrição')),
                ('pdf', models.FileField(help_text='Anexar somente arquivos com o pdf da situação.', upload_to=situacao.models.programa_pdf, verbose_name='PDF:')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('observacao', models.TextField(blank=True, default=None, help_text='...', max_length=255, null=True, verbose_name='Observação')),
                ('indices', models.ManyToManyField(help_text='Ligado a que índices:', related_name='nos_programas', to='situacao.Indice')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Programa',
                'verbose_name_plural': 'Programas',
                'ordering': ['referencia'],
            },
        ),
        migrations.CreateModel(
            name='Proposta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('arquivo', models.CharField(choices=[('interface.py', 'interface.py'), ('solucao.py', 'solucao.py'), ('entrada.txt', 'entrada.txt'), ('dados.txt', 'dados.txt')], max_length=25, verbose_name='Arquivo')),
                ('conteudo', models.TextField(blank=True, default=None, help_text='...', null=True, verbose_name='Conteúdo do arquivo')),
                ('ativo', models.BooleanField(default=True, help_text='...', verbose_name='Ativa')),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propostas', to='situacao.Programa')),
            ],
            options={
                'verbose_name': 'Proposta',
                'verbose_name_plural': 'Propostas',
            },
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('letra', models.CharField(help_text='...', max_length=5, verbose_name='Letra')),
                ('valor', models.CharField(help_text='...', max_length=55, verbose_name='Valor')),
            ],
            options={
                'verbose_name': 'Resposta',
                'verbose_name_plural': 'Respostas',
                'ordering': ['simulacao', 'letra'],
            },
        ),
        migrations.CreateModel(
            name='Simulacao',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('problema', models.ForeignKey(help_text='...', on_delete=django.db.models.deletion.CASCADE, related_name='simulacoes', to='situacao.Problema')),
            ],
            options={
                'verbose_name': 'Simulação',
                'verbose_name_plural': 'Simulações',
                'ordering': ['id', 'problema'],
            },
        ),
        migrations.CreateModel(
            name='Teste',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('entrada', models.TextField(blank=True, default=None, help_text='...', max_length=2555, null=True)),
                ('saida', models.TextField(blank=True, default=None, help_text='...', max_length=2555, null=True)),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testes', to='situacao.Programa')),
            ],
            options={
                'verbose_name': 'Teste',
                'verbose_name_plural': 'Testes',
                'ordering': ['programa'],
            },
        ),
        migrations.CreateModel(
            name='Texto',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('letra', models.CharField(help_text='...', max_length=5, verbose_name='Letra')),
                ('texto', models.TextField(blank=True, default=None, help_text='...', null=True, verbose_name='Texto:')),
                ('simulacao', models.ForeignKey(help_text='...', on_delete=django.db.models.deletion.CASCADE, related_name='textos', to='situacao.Simulacao')),
            ],
            options={
                'verbose_name': 'Texto',
                'verbose_name_plural': 'Textos',
                'ordering': ['simulacao', 'letra'],
            },
        ),
        migrations.CreateModel(
            name='ValorAleatorio',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('editado_em', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(help_text='...', max_length=25, verbose_name='Nome')),
                ('valor', models.CharField(help_text='...', max_length=25, verbose_name='Valor')),
                ('simulacao', models.ForeignKey(help_text='...', on_delete=django.db.models.deletion.CASCADE, related_name='valores_aleatorios', to='situacao.Simulacao')),
            ],
            options={
                'verbose_name': 'Valor Aleatorio',
                'verbose_name_plural': 'Valores Aleatorios',
                'ordering': ['simulacao', 'nome'],
            },
        ),
        migrations.AddField(
            model_name='resposta',
            name='simulacao',
            field=models.ForeignKey(help_text='...', on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='situacao.Simulacao'),
        ),
        migrations.AddField(
            model_name='arquivo',
            name='simulacao',
            field=models.ForeignKey(help_text='...', on_delete=django.db.models.deletion.CASCADE, related_name='arquivos', to='situacao.Simulacao'),
        ),
        migrations.AlterUniqueTogether(
            name='valoraleatorio',
            unique_together={('simulacao', 'nome')},
        ),
        migrations.AlterUniqueTogether(
            name='texto',
            unique_together={('simulacao', 'letra')},
        ),
        migrations.AlterUniqueTogether(
            name='resposta',
            unique_together={('simulacao', 'letra')},
        ),
        migrations.AlterUniqueTogether(
            name='proposta',
            unique_together={('programa', 'arquivo')},
        ),
        migrations.AlterUniqueTogether(
            name='arquivo',
            unique_together={('simulacao', 'letra')},
        ),
    ]
