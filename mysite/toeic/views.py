from django.shortcuts import render
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
            #groupe_etu = Group.objects.get(id='2')  # On ajoute l'utilisateur au groupe étudiant ici (id groupe étudiant = 2 )
            etu = Etudiant(numEtu=Utilisateur, mailEtu=form.cleaned_data.get('email'), classeEtu=form.cleaned_data.get('classeEtu'))
            etu.save()  # Sauvegarde de l'étudiant
            login(request, user) #Connexion au site
            estEtu = True
            request.session['estEtu'] = estEtu  # On mémorise le fait que c'est un étudiant en session
            return redirect('homepage')
    else:
        form = SignUpFormEtu(request.POST)
    return render(request, 'signup_etu.html', {'formEtu': form})


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
                #groupe = User.objects.filter(groups__name='etu', id=user.id) #On cherche si notre utilisateur est un étudiant
                #if not groupe: #Si aucun objet n'est retourné, il n'est pas étudiant donc prof
                    #estEtu = False
                #else:           #Sinon, c'est un étudiant
                    #estEtu =True
                #request.session['estEtu'] = estEtu #On mémorise cette information

                #if estEtu:
                  #  return redirect('homepage')
                #else:
                return redirect('homepage')
            else:
                error=True
                #ErrorMessage = "Username ou mot de passe incorrect"
    else:
        form= SignInForm()
    return render(request, 'signin.html', locals())

#---------------- Vue de déconnexion  ----------------
def logout_user(request):
    logout(request)
    return render(request, 'index.html')


#---------------- Vue mon compte ---------------------
def dashboard(request):
    utilisateur = User.objects.get(id=request.user.id)
    etu = Etudiant.objects.get(numEtu=request.user.id)
    return render(request, 'dashboard.html', locals())

