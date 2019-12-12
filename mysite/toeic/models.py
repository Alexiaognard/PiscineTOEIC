from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Etudiant(models.Model):
    numEtudiant = models.IntegerField(User, primary_key=True, help_text="Entrez votre numéro étudiant")
    nomEtudiant = models.CharField(max_length=30)
    prenomEtudiant = models.CharField(max_length=30)
    classeEtudiant = models.CharField(max_length=8)
    class Meta:
        db_table = 'etudiant'