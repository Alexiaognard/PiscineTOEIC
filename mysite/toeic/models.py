from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Classe(models.Model):
    Classe_choices = (
        ('IG3', 'IG3'),
        ('IG4', 'IG4'),
        ('IG5', 'IG5'),
        ('MAT3', 'MAT3'),
        ('MAT4', 'MAT4'),
        ('MAT5', 'MAT5'),
        ('PEIP1', 'PEIP1'),
        ('PEIP2', 'PEIP2'),
        ('GBA3', 'GBA3'),
        ('GBA4', 'GBA4'),
        ('GBA5', 'GBA5'),
        ('MI3', 'MI3'),
        ('MI4', 'MI4'),
        ('MI5', 'MI5')
    )

    numClasse = models.AutoField(primary_key=True)
    nomClasse = models.CharField(blank=True, max_length=5, choices=Classe_choices)
    promoClasse = models.IntegerField(blank=True,validators=[MinValueValidator(2020), MaxValueValidator(2100)])

    class Meta:
        db_table = 'classe'


class Etudiant(models.Model):
    numEtu = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    mailEtu = models.EmailField()
    classeEtu = models.ForeignKey(Classe, on_delete=models.CASCADE, db_column='numClasse')

    class Meta:
       db_table = 'etudiant'



class Appartenir(models.Model):
    numClasse = models.ForeignKey(Classe, on_delete=models.CASCADE, db_column='numClasse')
    numEtu = models.ForeignKey(Etudiant, on_delete=models.CASCADE, db_column='numEtu')

    class Meta:
        db_table = 'appartenir'

class Professeur(models.Model):
    numProf = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    mailProf = models.EmailField()
    class Meta:
        db_table = 'prof'


class Enseigner(models.Model):
    numProf=models.ForeignKey(Professeur, on_delete=models.CASCADE, db_column='numProf')
    numClasse=models.ForeignKey(Classe, on_delete=models.CASCADE, db_column='numClasse')
    class Meta:
        db_table='enseigner'


class Sujet(models.Model):
    numSujet = models.AutoField(primary_key=True)
    nomSujet = models.CharField(blank=True, max_length=20)
    mdpSujet = models.CharField(blank=True, max_length=20)

    class Meta:
        db_table = 'sujet'

class SessionToeic(models.Model):
    numSession = models.AutoField(primary_key=True)
    dateSession = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'sessiontoeic'

class Correspondre(models.Model):
    numSujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, db_column='numSujet')
    numSession = models.ForeignKey(SessionToeic, on_delete=models.CASCADE, db_column='numSession')


    class Meta:
        db_table = 'correspondre'
        unique_together = ('numSession','numSujet')

class PartieSujet(models.Model):
    numPartie = models.AutoField(primary_key=True)
    nomPartie = models.CharField(blank=True, max_length=10)
    dureePartie = models.BigIntegerField(blank=True)
    notePartie = models.IntegerField(blank=True,validators=[MinValueValidator(0), MaxValueValidator(100)])
    numSujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, db_column='numSujet')


    class Meta:
        db_table = 'partie'


class SousPartie(models.Model):
    numSousPartie = models.AutoField(primary_key=True)
    nomSousPartie = models.CharField(blank=True, max_length=10)
    numPartie = models.ForeignKey(PartieSujet, on_delete=models.CASCADE, db_column='numPartie')

    class Meta:
        db_table = 'souspartie'


class Composer(models.Model):
    numSujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, db_column='numSujet')
    numPartie = models.ForeignKey(PartieSujet, on_delete=models.CASCADE, db_column='numPartie')

    class Meta:
        db_table = 'composer'
        unique_together = ('numSujet', 'numPartie')


class Posseder(models.Model):
    numSousPartie = models.ForeignKey(SousPartie, on_delete=models.CASCADE, db_column='numSousPartie')
    numPartie = models.ForeignKey(PartieSujet, on_delete=models.CASCADE, db_column='numPartie')

    class Meta:
        db_table = 'posseder'
        unique_together = ('numSousPartie', 'numPartie')


class Travailler(models.Model):
    numEtu = models.ForeignKey(Etudiant, on_delete=models.CASCADE, db_column='numEtu')
    numSujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, db_column='numSujet')

    class Meta:
        db_table = 'travailler'

class Proposer(models.Model):
    numProf = models.ForeignKey(Professeur, on_delete=models.CASCADE, db_column='numProf')
    numSujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, db_column='numSujet')

    class Meta:
        db_table = 'proposer'
        unique_together = ('numProf', 'numSujet')


QUESTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),

    ]



class Question(models.Model):

    numQuestion = models.AutoField(primary_key=True)
    nomQuestion = models.CharField(blank=True, max_length=15)
    reponseQuestion = models.CharField(max_length=1,choices=QUESTION_CHOICES)
    numSousPartie = models.ForeignKey(SousPartie,on_delete=models.CASCADE, db_column='numSousPartie')

    class Meta:
        db_table = 'question'


class Repondre(models.Model):
    numQuestion = models.ForeignKey(Question,on_delete=models.CASCADE, db_column='numQuestion')
    numEtu = models.ForeignKey(Etudiant, on_delete=models.CASCADE, db_column='numEtu')

    class Meta:
        db_table='repondre'


class FaireSujet(models.Model):
    numSujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, db_column='numSujet')
    numEtu = models.ForeignKey(Etudiant, on_delete=models.CASCADE, db_column='numEtu')

    class Meta :
        db_table = 'fairesujet'

class Corriger(models.Model):
    numSujetEtu = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='numSujetEtu')
    numSujetProf = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='numSujetProf')
    class Meta:
        db_table ='corriger'