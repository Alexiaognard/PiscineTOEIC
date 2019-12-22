from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Etudiant(models.Model):
    numEtu = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    mailEtu = models.EmailField()
    classeEtu = models.CharField(blank=True, max_length=5)
    class Meta:
       db_table = 'etudiant'

class Professeur(models.Model):
    mailProf = models.EmailField()
    class Meta:
        db_table = 'prof'

QUESTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

class SujetEtu(models.Model):
    numSujet = models.AutoField(primary_key=True)
    nomSujet = models.CharField(blank=True, max_length=20)
    mdpSujet = models.CharField(blank=True, max_length=20)
    Q1 = models.CharField(
        max_length=2,
        choices=QUESTION_CHOICES,
        default= 'E',
    )
    Q2 = models.CharField(
        max_length=2,
        choices=QUESTION_CHOICES,
        default='E',
    )
    Q3 = models.CharField(
        max_length=2,
        choices=QUESTION_CHOICES,
        default='E',
    )
    Q4 = models.CharField(
        max_length=2,
        choices=QUESTION_CHOICES,
        default='E',
    )
    Q5 = models.CharField(
        max_length=2,
        choices=QUESTION_CHOICES,
        default='E',
    )
    class Meta :
        db_table = 'sujet_Etu'

