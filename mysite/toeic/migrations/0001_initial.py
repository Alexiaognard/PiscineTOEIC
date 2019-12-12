# Generated by Django 3.0 on 2019-12-12 15:15

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('numEtudiant', models.IntegerField(help_text='Entrez votre numéro étudiant', primary_key=True, serialize=False, verbose_name=django.contrib.auth.models.User)),
                ('nomEtudiant', models.CharField(max_length=30)),
                ('prenomEtudiant', models.CharField(max_length=30)),
                ('classeEtudiant', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'etudiant',
            },
        ),
    ]
