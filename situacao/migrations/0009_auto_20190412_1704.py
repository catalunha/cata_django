# Generated by Django 2.1.3 on 2019-04-12 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situacao', '0008_auto_20181213_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
        migrations.AddField(
            model_name='indice',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
        migrations.AddField(
            model_name='resposta',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
        migrations.AddField(
            model_name='simulacao',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
        migrations.AddField(
            model_name='teste',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
        migrations.AddField(
            model_name='texto',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
        migrations.AddField(
            model_name='valoraleatorio',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
    ]