# Generated by Django 2.1.3 on 2019-04-12 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ementa',
            name='ativo',
            field=models.BooleanField(default=True, help_text='...'),
        ),
    ]
