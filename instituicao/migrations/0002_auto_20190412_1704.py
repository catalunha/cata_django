# Generated by Django 2.1.3 on 2019-04-12 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instituicao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituicao',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
    ]
