"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from toeic import views
from django.conf import settings


urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('signup/etudiant', views.signup_etu, name='signupEtu'),
    path('monCompte', views.monCompte_etu, name='dashboardEtu'),
    path('dashboard', views.monCompte_prof, name='dashboardProf'),
    path('signup/professeur', views.signup_prof, name='signupProf'),
    path('create/subject_prof', views.create_subject_prof, name='create_subject_prof'),
    path('create/subject/<int:idSujet>', views.create_subject, name='create_subject'),
    path('read/subject_prof/<int:idSujet>', views.read_subject_prof, name='read_subject_prof'),
    path('read/subject/<int:idSujet>', views.read_subject, name='read_subject'),
    path('create/subject_etu/', views.create_subject_etu, name='create_subject_etu'),
    path('create/subject_etu/<int:idSujet>', views.make_subject_etu, name='make_subject_etu'),
    path('read/subject_etu/<int:idSujet>', views.read_subject_etu, name='read_subject_etu'),
    path('corriger/<int:idSujet>',views.corriger_sujet, name='corriger_sujet'),
    path('listSubjects', views.lire_sujets, name='voir_sujet'),
    path('updateEtu', views.updateEtu, name='updateEtu'),
    path('updateProf', views.updateProf, name='updateProf'),
    path('deleteEtu', views.delete_etu, name='delete_etu'),
    path('stats_par_sujet_etu/<int:idSujet>', views.stats_par_sujet_etu, name='stats_par_sujet_etu'),
    path('stats_par_partie_prof', views.stats_par_partie_prof, name='stats_par_partie_prof'),
    path('stats_par_sujet_prof/<int:idSujet>', views.stats_par_sujet_prof, name='stats_par_sujet_prof'),
    path('liste_sujet_prof', views.liste_sujet_prof, name='liste_sujet_prof'),
    path('listeClasse', views.listeclasse, name='listeClasse'),
    path('statsClasses/<int:numClasse>', views.stats_classe_prof, name='statsClasses'),
    path('stats_par_partie_etu', views.stats_par_partie_etu, name='stats_par_partie_etu'),
    path('stats', views.stats, name='stats'),
    path('stats_par_partie_etu_prof/<str:idEtu>', views.stats_par_partie_etu_prof, name='stats_par_partie_etu_prof'),
    path('listeEtuClasse/<int:numClasse>', views.listeEtuClasse, name='listeEtuClasse'),
    path('listeEtu', views.listeEtu, name='listeEtu')
   
]
