# Generated by Django 2.1.3 on 2019-04-12 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instituicao', '0002_auto_20190412_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instituicao',
            name='ativo',
        ),
    ]
