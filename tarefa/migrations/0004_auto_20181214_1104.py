# Generated by Django 2.1.3 on 2018-12-14 14:04

from django.db import migrations, models
import tarefa.models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefa', '0003_auto_20181112_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anexo',
            name='anexo',
            field=models.FileField(blank=True, default=None, help_text='...', max_length=255, upload_to=tarefa.models.arquivo_questao, verbose_name='Arquivo:'),
        ),
    ]
