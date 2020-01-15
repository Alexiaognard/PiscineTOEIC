from django.contrib import admin

# Register your models here.
from toeic.models import *

admin.site.register(Classe)
admin.site.register(Etudiant)
admin.site.register(Professeur)
admin.site.register(Sujet)
admin.site.register(PartieSujet)
admin.site.register(Question)
admin.site.register(Corriger)
admin.site.register(FaireSujet)
admin.site.register(Composer)
admin.site.register(Proposer)

