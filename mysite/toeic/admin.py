from django.contrib import admin

# Register your models here.
from toeic.models import Classe, Etudiant, Professeur, Sujet, PartieSujet

admin.site.register(Classe)
admin.site.register(Etudiant)
admin.site.register(Professeur)
admin.site.register(Sujet)
admin.site.register(PartieSujet)