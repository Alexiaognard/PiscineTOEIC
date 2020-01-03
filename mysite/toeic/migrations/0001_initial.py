# Generated by Django 3.0 on 2020-01-03 09:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('numClasse', models.AutoField(primary_key=True, serialize=False)),
                ('nomClasse', models.CharField(blank=True, choices=[('IG3', 'IG3'), ('IG4', 'IG4'), ('IG5', 'IG5'), ('MAT3', 'MAT3'), ('MAT4', 'MAT4'), ('MAT5', 'MAT5'), ('PEIP1', 'PEIP1'), ('PEIP2', 'PEIP2'), ('GBA3', 'GBA3'), ('GBA4', 'GBA4'), ('GBA5', 'GBA5'), ('MI3', 'MI3'), ('MI4', 'MI4'), ('MI5', 'MI5')], max_length=5)),
                ('promoClasse', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(2020), django.core.validators.MaxValueValidator(2100)])),
            ],
            options={
                'db_table': 'classe',
            },
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('numEtu', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mailEtu', models.EmailField(max_length=254)),
                ('classeEtu', models.ForeignKey(db_column='numClasse', on_delete=django.db.models.deletion.CASCADE, to='toeic.Classe')),
            ],
            options={
                'db_table': 'etudiant',
            },
        ),
        migrations.CreateModel(
            name='PartieSujet',
            fields=[
                ('numPartie', models.AutoField(primary_key=True, serialize=False)),
                ('nomPartie', models.CharField(blank=True, max_length=10)),
                ('dureePartie', models.BigIntegerField(blank=True)),
                ('notePartie', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'db_table': 'partie',
            },
        ),
        migrations.CreateModel(
            name='Professeur',
            fields=[
                ('numProf', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mailProf', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'prof',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('numQuestion', models.AutoField(primary_key=True, serialize=False)),
                ('nomQuestion', models.CharField(blank=True, max_length=15)),
                ('reponseQuestion', models.IntegerField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='SessionToeic',
            fields=[
                ('numSession', models.AutoField(primary_key=True, serialize=False)),
                ('dateSession', models.DateTimeField()),
            ],
            options={
                'db_table': 'sessiontoeic',
            },
        ),
        migrations.CreateModel(
            name='Sujet',
            fields=[
                ('numSujet', models.AutoField(primary_key=True, serialize=False)),
                ('nomSujet', models.CharField(blank=True, max_length=20)),
                ('mdpSujet', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'db_table': 'sujet',
            },
        ),
        migrations.CreateModel(
            name='Travailler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numEtu', models.ForeignKey(db_column='numEtu', on_delete=django.db.models.deletion.CASCADE, to='toeic.Etudiant')),
                ('numSujet', models.ForeignKey(db_column='numSujet', on_delete=django.db.models.deletion.CASCADE, to='toeic.Sujet')),
            ],
            options={
                'db_table': 'travailler',
            },
        ),
        migrations.CreateModel(
            name='SousPartie',
            fields=[
                ('numSousPartie', models.AutoField(primary_key=True, serialize=False)),
                ('nomSousPartie', models.CharField(blank=True, max_length=10)),
                ('numPartie', models.ForeignKey(db_column='numPartie', on_delete=django.db.models.deletion.CASCADE, to='toeic.PartieSujet')),
            ],
            options={
                'db_table': 'souspartie',
            },
        ),
        migrations.CreateModel(
            name='Repondre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numEtu', models.ForeignKey(db_column='numEtu', on_delete=django.db.models.deletion.CASCADE, to='toeic.Etudiant')),
                ('numQuestion', models.ForeignKey(db_column='numQuestion', on_delete=django.db.models.deletion.CASCADE, to='toeic.Question')),
            ],
            options={
                'db_table': 'repondre',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='numSousPartie',
            field=models.ForeignKey(db_column='numSousPartie', on_delete=django.db.models.deletion.CASCADE, to='toeic.SousPartie'),
        ),
        migrations.AddField(
            model_name='partiesujet',
            name='numSujet',
            field=models.ForeignKey(db_column='numSujet', on_delete=django.db.models.deletion.CASCADE, to='toeic.Sujet'),
        ),
        migrations.CreateModel(
            name='Appartenir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numClasse', models.ForeignKey(db_column='numClasse', on_delete=django.db.models.deletion.CASCADE, to='toeic.Classe')),
                ('numEtu', models.ForeignKey(db_column='numEtu', on_delete=django.db.models.deletion.CASCADE, to='toeic.Etudiant')),
            ],
            options={
                'db_table': 'appartenir',
            },
        ),
        migrations.CreateModel(
            name='Proposer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numProf', models.ForeignKey(db_column='numProf', on_delete=django.db.models.deletion.CASCADE, to='toeic.Professeur')),
                ('numSujet', models.ForeignKey(db_column='numSujet', on_delete=django.db.models.deletion.CASCADE, to='toeic.Sujet')),
            ],
            options={
                'db_table': 'proposer',
                'unique_together': {('numProf', 'numSujet')},
            },
        ),
        migrations.CreateModel(
            name='Posseder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numPartie', models.ForeignKey(db_column='numPartie', on_delete=django.db.models.deletion.CASCADE, to='toeic.PartieSujet')),
                ('numSousPartie', models.ForeignKey(db_column='numSousPartie', on_delete=django.db.models.deletion.CASCADE, to='toeic.SousPartie')),
            ],
            options={
                'db_table': 'posseder',
                'unique_together': {('numSousPartie', 'numPartie')},
            },
        ),
        migrations.CreateModel(
            name='Correspondre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numSession', models.ForeignKey(db_column='numSession', on_delete=django.db.models.deletion.CASCADE, to='toeic.SessionToeic')),
                ('numSujet', models.ForeignKey(db_column='numSujet', on_delete=django.db.models.deletion.CASCADE, to='toeic.Sujet')),
            ],
            options={
                'db_table': 'correspondre',
                'unique_together': {('numSession', 'numSujet')},
            },
        ),
        migrations.CreateModel(
            name='Composer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numPartie', models.ForeignKey(db_column='numPartie', on_delete=django.db.models.deletion.CASCADE, to='toeic.PartieSujet')),
                ('numSujet', models.ForeignKey(db_column='numSujet', on_delete=django.db.models.deletion.CASCADE, to='toeic.Sujet')),
            ],
            options={
                'db_table': 'composer',
                'unique_together': {('numSujet', 'numPartie')},
            },
        ),
    ]
