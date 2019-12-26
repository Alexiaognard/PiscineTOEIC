
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from toeic.forms import *
from toeic.models import *

# Create your views here.
#-------------- Vue de la page d'accueil -----------------
def homepage(request):
    return render(request, 'homepage.html')

#---------------- Vue de création de comptes Etudiant/Prof  ----------------
#Creation d'un compte étudiant
def signup_etu(request):
    if request.method == 'POST':
        form = SignUpFormEtu(request.POST)
        if form.is_valid():
            form.save() #Sauvegarde/Creation d'un utilisateur de base
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) #Authentification de l'utilisateur
            Utilisateur = User.objects.get(username=username)
            classEtu = Classe(nomClasse=form.cleaned_data.get('classeEtu'),promoClasse=form.cleaned_data.get('promoEtu'))
            classEtu.save()
            etu = Etudiant(numEtu=Utilisateur, mailEtu=form.cleaned_data.get('email'), classeEtu=classEtu)
            etu.save()  # Sauvegarde de l'étudiant
            login(request, user) #Connexion au site
            estEtu = True
            request.session['estEtu'] = estEtu  # On mémorise le fait que c'est un étudiant en session
            return redirect('homepage')
    else:
        form = SignUpFormEtu(request.POST)
    return render(request, 'signup_etu.html', {'formEtu': form})


#Creation d'un compte prof
def signup_prof(request):
    if request.method == 'POST':
        form = SignUpFormProf(request.POST)
        if form.is_valid():
            form.save() #Sauvegarde/Creation d'un utilisateur de base
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) #Authentification de l'utilisateur
            Utilisateur = User.objects.get(username=username)
            prof = Professeur(numProf=Utilisateur, mailProf=form.cleaned_data.get('email'))
            prof.save()  # Sauvegarde du professeur
            login(request, user) #Connexion au site
            estEtu = False
            request.session['estEtu'] = estEtu  # On mémorise le fait que c'est un professeur en session
            return redirect('homepage')
    else:
        form = SignUpFormProf(request.POST)
    return render(request, 'signup_prof.html', {'formProf': form})
#---------------- Vue de connexion  ----------------


def login_user(request):
    error=False
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password"]
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request,user)
                return redirect('homepage')
            else:
                error=True
                #ErrorMessage = "Username ou mot de passe incorrect"
    else:
        form = SignInForm()
    return render(request, 'signin.html', locals())

#---------------- Vue de déconnexion  ----------------
def logout_user(request):
    logout(request)
    return render(request, 'index.html')


#---------------- Vue mon compte ---------------------
def monCompte_etu(request):
    utilisateur = User.objects.get(id=request.user.id)
    user = Etudiant.objects.get(numEtu=request.user.id)
    return render(request, 'dashboard.html', locals())

def monCompte_prof(request):
    utilisateur = User.objects.get(id=request.user.id)
    user = Professeur.objects.get(numProf=request.user.id)
    return render(request, 'dashboard.html', locals())








