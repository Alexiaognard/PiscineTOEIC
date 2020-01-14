
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from toeic.forms import *
from toeic.models import *
import datetime
import numpy


groupe_prof = Group(id='1',name='professeur')
groupe_prof.save()
groupe_etu = Group(id='2',name='etudiant')
groupe_etu.save()
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
            try:
                classEtu = Classe.objects.get(nomClasse=form.cleaned_data.get('classeEtu'),promoClasse=form.cleaned_data.get('promoEtu'))

            except:
                classEtu = Classe(nomClasse=form.cleaned_data.get('classeEtu'), promoClasse=form.cleaned_data.get('promoEtu'))
                classEtu.save()
            groupe_etu = Group.objects.get(id='2')  # On ajoute l'utilisateur au groupe étudiant ici (id groupe étudiant = 2 )
            Utilisateur.groups.add(groupe_etu)
            etu = Etudiant(numEtu=Utilisateur, mailEtu=form.cleaned_data.get('email'), classeEtu=classEtu)
            etu.save()  # Sauvegarde de l'étudiant
            appartenir = Appartenir(numClasse=classEtu,numEtu=etu)
            appartenir.save()
            login(request, user) #Connexion au site
            estEtu = True
            request.session[estEtu] = estEtu  # On mémorise le fait que c'est un étudiant en session
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
            groupe_etu = Group.objects.get(id='1')  # On ajoute l'utilisateur au groupe professeur ici (id groupe professeur = 1 )
            Utilisateur.groups.add(groupe_etu)
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
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password"]
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request,user)
                groupe = User.objects.filter(groups__name='etudiant', id=user.id) #On cherche si notre utilisateur est un étudiant
                if not groupe: #Si aucun objet n'est retourné, il n'est pas étudiant
                    estEtu = False
                else:           #Sinon, c'est un client
                    estEtu =True
                request.session['estEtu'] = estEtu  #On mémorise cette information

                if estEtu:
                    return redirect('homepage')
                else:
                    return redirect('homepage')
    else:
        form = SignInForm(request.POST)
    return render(request, 'signin.html', locals())

#---------------- Vue de déconnexion  ----------------
def logout_user(request):
    logout(request)
    return render(request, 'index.html')


#---------------- Vue mon compte ---------------------
@login_required
def monCompte_etu(request):
    if not request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        utilisateur = User.objects.get(id=request.user.id)
        user = Etudiant.objects.get(numEtu=request.user.id)
        return render(request, 'dashboard.html', locals())

@login_required
def monCompte_prof(request):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        utilisateur = User.objects.get(id=request.user.id)
        user = Professeur.objects.get(numProf=request.user.id)
        return render(request, 'dashboard.html', locals())

#---------------- Vue création de sujet de TOEIC ---------------------
@login_required
def create_subject_prof(request):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        if request.method == 'POST':
            utilisateur=User.objects.get(id=request.user.id)

            form = CreateSubjectForm(request.POST)
            if form.is_valid():
                sub=Sujet(nomSujet=form.cleaned_data["nomSujet"],mdpSujet=form.cleaned_data["mdpSujet"])
                sub.save()
                print("prof",sub)
                return read_subject_prof(request,sub.numSujet)
        else:
            form = CreateSubjectForm()
        return render(request, 'create_subject_prof.html', locals())


@login_required
def create_subject(request,idSujet):
        if request.method == 'POST':
            prof=Professeur.objects.get(numProf=request.user.id)

            form = RemplirSujetForm(request.POST)


            if form.is_valid():
                sub = Sujet.objects.get(numSujet=idSujet)

                prop = Proposer(numProf=prof,numSujet=sub)
                prop.save()

                p1 = PartieSujet(nomPartie="Listening", dureePartie=50000,notePartie=0,numSujet=sub)
                p1.save()
                p2 = PartieSujet(nomPartie="Reading", dureePartie=50000, notePartie=0, numSujet=sub)
                p2.save()


                comp1 = Composer(numSujet=sub,numPartie=p1)
                comp1.save()
                comp2 = Composer(numSujet=sub, numPartie=p2)
                comp2.save()


                sp1 = SousPartie(nomSousPartie="Part 1",numPartie=p1)
                sp1.save()
                sp2 = SousPartie(nomSousPartie="Part 2", numPartie=p1)
                sp2.save()
                sp3 = SousPartie(nomSousPartie="Part 3", numPartie=p1)
                sp3.save()
                sp4 = SousPartie(nomSousPartie="Part 4", numPartie=p1)
                sp4.save()
                sp5 = SousPartie(nomSousPartie="Part 5", numPartie=p2)
                sp5.save()
                sp6 = SousPartie(nomSousPartie="Part 6", numPartie=p2)
                sp6.save()
                sp7 = SousPartie(nomSousPartie="Part 7", numPartie=p2)
                sp7.save()

                pos1 = Posseder(numSousPartie=sp1,numPartie=p1)
                pos1.save()
                pos2 = Posseder(numSousPartie=sp2, numPartie=p1)
                pos2.save()
                pos3 = Posseder(numSousPartie=sp3, numPartie=p1)
                pos3.save()
                pos4 = Posseder(numSousPartie=sp4, numPartie=p1)
                pos4.save()
                pos5 = Posseder(numSousPartie=sp5, numPartie=p2)
                pos5.save()
                pos6 = Posseder(numSousPartie=sp6, numPartie=p2)
                pos6.save()
                pos7 = Posseder(numSousPartie=sp7, numPartie=p2)
                pos7.save()


                Q1 = Question(nomQuestion='Q1', reponseQuestion=form.cleaned_data.get('Q1'), numSousPartie=sp1)
                Q1.save()
                Q2 = Question(nomQuestion='Q2', reponseQuestion=form.cleaned_data.get('Q2'), numSousPartie=sp1)
                Q2.save()
                Q3 = Question(nomQuestion='Q3', reponseQuestion=form.cleaned_data.get('Q3'), numSousPartie=sp1)
                Q3.save()
                Q4 = Question(nomQuestion='Q4', reponseQuestion=form.cleaned_data.get('Q4'), numSousPartie=sp1)
                Q4.save()
                Q5 = Question(nomQuestion='Q5', reponseQuestion=form.cleaned_data.get('Q5'), numSousPartie=sp1)
                Q5.save()
                Q6 = Question(nomQuestion='Q6', reponseQuestion=form.cleaned_data.get('Q6'), numSousPartie=sp1)
                Q6.save()
                Q7 = Question(nomQuestion='Q7', reponseQuestion=form.cleaned_data.get('Q7'), numSousPartie=sp2)
                Q7.save()
                Q8 = Question(nomQuestion='Q8', reponseQuestion=form.cleaned_data.get('Q8'), numSousPartie=sp2)
                Q8.save()
                Q9 = Question(nomQuestion='Q9', reponseQuestion=form.cleaned_data.get('Q9'), numSousPartie=sp2)
                Q9.save()
                Q10 = Question(nomQuestion='Q10', reponseQuestion=form.cleaned_data.get('Q10'), numSousPartie=sp2)
                Q10.save()
                Q11 = Question(nomQuestion='Q11', reponseQuestion=form.cleaned_data.get('Q11'), numSousPartie=sp2)
                Q11.save()
                Q12 = Question(nomQuestion='Q12', reponseQuestion=form.cleaned_data.get('Q12'), numSousPartie=sp2)
                Q12.save()
                Q13 = Question(nomQuestion='Q13', reponseQuestion=form.cleaned_data.get('Q13'), numSousPartie=sp2)
                Q13.save()
                Q14 = Question(nomQuestion='Q14', reponseQuestion=form.cleaned_data.get('Q14'), numSousPartie=sp2)
                Q14.save()
                Q15 = Question(nomQuestion='Q15', reponseQuestion=form.cleaned_data.get('Q15'), numSousPartie=sp2)
                Q15.save()
                Q16 = Question(nomQuestion='Q16', reponseQuestion=form.cleaned_data.get('Q16'), numSousPartie=sp2)
                Q16.save()
                Q17 = Question(nomQuestion='Q17', reponseQuestion=form.cleaned_data.get('Q17'), numSousPartie=sp2)
                Q17.save()
                Q18 = Question(nomQuestion='Q18', reponseQuestion=form.cleaned_data.get('Q18'), numSousPartie=sp2)
                Q18.save()
                Q19 = Question(nomQuestion='Q19', reponseQuestion=form.cleaned_data.get('Q19'), numSousPartie=sp2)
                Q19.save()
                Q20 = Question(nomQuestion='Q20', reponseQuestion=form.cleaned_data.get('Q20'), numSousPartie=sp2)
                Q20.save()
                Q21 = Question(nomQuestion='Q21', reponseQuestion=form.cleaned_data.get('Q21'), numSousPartie=sp2)
                Q21.save()
                Q22 = Question(nomQuestion='Q22', reponseQuestion=form.cleaned_data.get('Q22'), numSousPartie=sp2)
                Q22.save()
                Q23 = Question(nomQuestion='Q23', reponseQuestion=form.cleaned_data.get('Q23'), numSousPartie=sp2)
                Q23.save()
                Q24 = Question(nomQuestion='Q24', reponseQuestion=form.cleaned_data.get('Q24'), numSousPartie=sp2)
                Q24.save()
                Q25 = Question(nomQuestion='Q25', reponseQuestion=form.cleaned_data.get('Q25'), numSousPartie=sp2)
                Q25.save()
                Q26 = Question(nomQuestion='Q26', reponseQuestion=form.cleaned_data.get('Q26'), numSousPartie=sp2)
                Q26.save()
                Q27 = Question(nomQuestion='Q27', reponseQuestion=form.cleaned_data.get('Q27'), numSousPartie=sp2)
                Q27.save()
                Q28 = Question(nomQuestion='Q28', reponseQuestion=form.cleaned_data.get('Q28'), numSousPartie=sp2)
                Q28.save()
                Q29 = Question(nomQuestion='Q29', reponseQuestion=form.cleaned_data.get('Q29'), numSousPartie=sp2)
                Q29.save()
                Q30 = Question(nomQuestion='Q30', reponseQuestion=form.cleaned_data.get('Q30'), numSousPartie=sp2)
                Q30.save()
                Q31 = Question(nomQuestion='Q31', reponseQuestion=form.cleaned_data.get('Q31'), numSousPartie=sp2)
                Q31.save()
                Q32 = Question(nomQuestion='Q32', reponseQuestion=form.cleaned_data.get('Q32'), numSousPartie=sp3)
                Q32.save()
                Q33 = Question(nomQuestion='Q33', reponseQuestion=form.cleaned_data.get('Q33'), numSousPartie=sp3)
                Q33.save()
                Q34 = Question(nomQuestion='Q34', reponseQuestion=form.cleaned_data.get('Q34'), numSousPartie=sp3)
                Q34.save()
                Q35 = Question(nomQuestion='Q35', reponseQuestion=form.cleaned_data.get('Q35'), numSousPartie=sp3)
                Q35.save()
                Q36 = Question(nomQuestion='Q36', reponseQuestion=form.cleaned_data.get('Q36'), numSousPartie=sp3)
                Q36.save()
                Q37 = Question(nomQuestion='Q37', reponseQuestion=form.cleaned_data.get('Q37'), numSousPartie=sp3)
                Q37.save()
                Q38 = Question(nomQuestion='Q38', reponseQuestion=form.cleaned_data.get('Q38'), numSousPartie=sp3)
                Q38.save()
                Q39 = Question(nomQuestion='Q39', reponseQuestion=form.cleaned_data.get('Q39'), numSousPartie=sp3)
                Q39.save()
                Q40 = Question(nomQuestion='Q40', reponseQuestion=form.cleaned_data.get('Q40'), numSousPartie=sp3)
                Q40.save()
                Q41 = Question(nomQuestion='Q41', reponseQuestion=form.cleaned_data.get('Q41'), numSousPartie=sp3)
                Q41.save()
                Q42 = Question(nomQuestion='Q42', reponseQuestion=form.cleaned_data.get('Q42'), numSousPartie=sp3)
                Q42.save()
                Q43 = Question(nomQuestion='Q43', reponseQuestion=form.cleaned_data.get('Q43'), numSousPartie=sp3)
                Q43.save()
                Q44 = Question(nomQuestion='Q44', reponseQuestion=form.cleaned_data.get('Q44'), numSousPartie=sp3)
                Q44.save()
                Q45 = Question(nomQuestion='Q45', reponseQuestion=form.cleaned_data.get('Q45'), numSousPartie=sp3)
                Q45.save()
                Q46 = Question(nomQuestion='Q46', reponseQuestion=form.cleaned_data.get('Q46'), numSousPartie=sp3)
                Q46.save()
                Q47 = Question(nomQuestion='Q47', reponseQuestion=form.cleaned_data.get('Q47'), numSousPartie=sp3)
                Q47.save()
                Q48 = Question(nomQuestion='Q48', reponseQuestion=form.cleaned_data.get('Q48'), numSousPartie=sp3)
                Q48.save()
                Q49 = Question(nomQuestion='Q49', reponseQuestion=form.cleaned_data.get('Q49'), numSousPartie=sp3)
                Q49.save()
                Q50 = Question(nomQuestion='Q50', reponseQuestion=form.cleaned_data.get('Q50'), numSousPartie=sp3)
                Q50.save()
                Q51 = Question(nomQuestion='Q51', reponseQuestion=form.cleaned_data.get('Q51'), numSousPartie=sp3)
                Q51.save()
                Q52 = Question(nomQuestion='Q52', reponseQuestion=form.cleaned_data.get('Q52'), numSousPartie=sp3)
                Q52.save()
                Q53 = Question(nomQuestion='Q53', reponseQuestion=form.cleaned_data.get('Q53'), numSousPartie=sp3)
                Q53.save()
                Q54 = Question(nomQuestion='Q54', reponseQuestion=form.cleaned_data.get('Q54'), numSousPartie=sp3)
                Q54.save()
                Q55 = Question(nomQuestion='Q55', reponseQuestion=form.cleaned_data.get('Q55'), numSousPartie=sp3)
                Q55.save()
                Q56 = Question(nomQuestion='Q56', reponseQuestion=form.cleaned_data.get('Q56'), numSousPartie=sp3)
                Q56.save()
                Q57 = Question(nomQuestion='Q57', reponseQuestion=form.cleaned_data.get('Q57'), numSousPartie=sp3)
                Q57.save()
                Q58 = Question(nomQuestion='Q58', reponseQuestion=form.cleaned_data.get('Q58'), numSousPartie=sp3)
                Q58.save()
                Q59 = Question(nomQuestion='Q59', reponseQuestion=form.cleaned_data.get('Q59'), numSousPartie=sp3)
                Q59.save()
                Q60 = Question(nomQuestion='Q60', reponseQuestion=form.cleaned_data.get('Q60'), numSousPartie=sp3)
                Q60.save()
                Q61 = Question(nomQuestion='Q61', reponseQuestion=form.cleaned_data.get('Q61'), numSousPartie=sp3)
                Q61.save()
                Q62 = Question(nomQuestion='Q62', reponseQuestion=form.cleaned_data.get('Q62'), numSousPartie=sp3)
                Q62.save()
                Q63 = Question(nomQuestion='Q63', reponseQuestion=form.cleaned_data.get('Q63'), numSousPartie=sp3)
                Q63.save()
                Q64 = Question(nomQuestion='Q64', reponseQuestion=form.cleaned_data.get('Q64'), numSousPartie=sp3)
                Q64.save()
                Q65 = Question(nomQuestion='Q65', reponseQuestion=form.cleaned_data.get('Q65'), numSousPartie=sp3)
                Q65.save()
                Q66 = Question(nomQuestion='Q66', reponseQuestion=form.cleaned_data.get('Q66'), numSousPartie=sp3)
                Q66.save()
                Q67 = Question(nomQuestion='Q67', reponseQuestion=form.cleaned_data.get('Q67'), numSousPartie=sp3)
                Q67.save()
                Q68 = Question(nomQuestion='Q68', reponseQuestion=form.cleaned_data.get('Q68'), numSousPartie=sp3)
                Q68.save()
                Q69 = Question(nomQuestion='Q69', reponseQuestion=form.cleaned_data.get('Q69'), numSousPartie=sp3)
                Q69.save()
                Q70 = Question(nomQuestion='Q70', reponseQuestion=form.cleaned_data.get('Q70'), numSousPartie=sp3)
                Q70.save()
                Q71 = Question(nomQuestion='Q71', reponseQuestion=form.cleaned_data.get('Q71'), numSousPartie=sp4)
                Q71.save()
                Q72 = Question(nomQuestion='Q72', reponseQuestion=form.cleaned_data.get('Q72'), numSousPartie=sp4)
                Q72.save()
                Q73 = Question(nomQuestion='Q73', reponseQuestion=form.cleaned_data.get('Q73'), numSousPartie=sp4)
                Q73.save()
                Q74 = Question(nomQuestion='Q74', reponseQuestion=form.cleaned_data.get('Q74'), numSousPartie=sp4)
                Q74.save()
                Q75 = Question(nomQuestion='Q75', reponseQuestion=form.cleaned_data.get('Q75'), numSousPartie=sp4)
                Q75.save()
                Q76 = Question(nomQuestion='Q76', reponseQuestion=form.cleaned_data.get('Q76'), numSousPartie=sp4)
                Q76.save()
                Q77 = Question(nomQuestion='Q77', reponseQuestion=form.cleaned_data.get('Q77'), numSousPartie=sp4)
                Q77.save()
                Q78 = Question(nomQuestion='Q78', reponseQuestion=form.cleaned_data.get('Q78'), numSousPartie=sp4)
                Q78.save()
                Q79 = Question(nomQuestion='Q79', reponseQuestion=form.cleaned_data.get('Q79'), numSousPartie=sp4)
                Q79.save()
                Q80 = Question(nomQuestion='Q80', reponseQuestion=form.cleaned_data.get('Q80'), numSousPartie=sp4)
                Q80.save()
                Q81 = Question(nomQuestion='Q81', reponseQuestion=form.cleaned_data.get('Q81'), numSousPartie=sp4)
                Q81.save()
                Q82 = Question(nomQuestion='Q82', reponseQuestion=form.cleaned_data.get('Q82'), numSousPartie=sp4)
                Q82.save()
                Q83 = Question(nomQuestion='Q83', reponseQuestion=form.cleaned_data.get('Q83'), numSousPartie=sp4)
                Q83.save()
                Q84 = Question(nomQuestion='Q84', reponseQuestion=form.cleaned_data.get('Q84'), numSousPartie=sp4)
                Q84.save()
                Q85 = Question(nomQuestion='Q85', reponseQuestion=form.cleaned_data.get('Q85'), numSousPartie=sp4)
                Q85.save()
                Q86 = Question(nomQuestion='Q86', reponseQuestion=form.cleaned_data.get('Q86'), numSousPartie=sp4)
                Q86.save()
                Q87 = Question(nomQuestion='Q87', reponseQuestion=form.cleaned_data.get('Q87'), numSousPartie=sp4)
                Q87.save()
                Q88 = Question(nomQuestion='Q88', reponseQuestion=form.cleaned_data.get('Q88'), numSousPartie=sp4)
                Q88.save()
                Q89 = Question(nomQuestion='Q89', reponseQuestion=form.cleaned_data.get('Q89'), numSousPartie=sp4)
                Q89.save()
                Q90 = Question(nomQuestion='Q90', reponseQuestion=form.cleaned_data.get('Q90'), numSousPartie=sp4)
                Q90.save()
                Q91 = Question(nomQuestion='Q91', reponseQuestion=form.cleaned_data.get('Q91'), numSousPartie=sp4)
                Q91.save()
                Q92 = Question(nomQuestion='Q92', reponseQuestion=form.cleaned_data.get('Q92'), numSousPartie=sp4)
                Q92.save()
                Q93 = Question(nomQuestion='Q93', reponseQuestion=form.cleaned_data.get('Q93'), numSousPartie=sp4)
                Q93.save()
                Q94 = Question(nomQuestion='Q94', reponseQuestion=form.cleaned_data.get('Q94'), numSousPartie=sp4)
                Q94.save()
                Q95 = Question(nomQuestion='Q95', reponseQuestion=form.cleaned_data.get('Q95'), numSousPartie=sp4)
                Q95.save()
                Q96 = Question(nomQuestion='Q96', reponseQuestion=form.cleaned_data.get('Q96'), numSousPartie=sp4)
                Q96.save()
                Q97 = Question(nomQuestion='Q97', reponseQuestion=form.cleaned_data.get('Q97'), numSousPartie=sp4)
                Q97.save()
                Q98 = Question(nomQuestion='Q98', reponseQuestion=form.cleaned_data.get('Q98'), numSousPartie=sp4)
                Q98.save()
                Q99 = Question(nomQuestion='Q99', reponseQuestion=form.cleaned_data.get('Q99'), numSousPartie=sp4)
                Q99.save()
                Q100 = Question(nomQuestion='Q100', reponseQuestion=form.cleaned_data.get('Q100'), numSousPartie=sp4)
                Q100.save()
                Q101 = Question(nomQuestion='Q101', reponseQuestion=form.cleaned_data.get('Q101'), numSousPartie=sp5)
                Q101.save()
                Q102 = Question(nomQuestion='Q102', reponseQuestion=form.cleaned_data.get('Q102'), numSousPartie=sp5)
                Q102.save()
                Q103 = Question(nomQuestion='Q103', reponseQuestion=form.cleaned_data.get('Q103'), numSousPartie=sp5)
                Q103.save()
                Q104 = Question(nomQuestion='Q104', reponseQuestion=form.cleaned_data.get('Q104'), numSousPartie=sp5)
                Q104.save()
                Q105 = Question(nomQuestion='Q105', reponseQuestion=form.cleaned_data.get('Q105'), numSousPartie=sp5)
                Q105.save()
                Q106 = Question(nomQuestion='Q106', reponseQuestion=form.cleaned_data.get('Q106'), numSousPartie=sp5)
                Q106.save()
                Q107 = Question(nomQuestion='Q107', reponseQuestion=form.cleaned_data.get('Q107'), numSousPartie=sp5)
                Q107.save()
                Q108 = Question(nomQuestion='Q108', reponseQuestion=form.cleaned_data.get('Q108'), numSousPartie=sp5)
                Q108.save()
                Q109 = Question(nomQuestion='Q109', reponseQuestion=form.cleaned_data.get('Q109'), numSousPartie=sp5)
                Q109.save()
                Q110 = Question(nomQuestion='Q110', reponseQuestion=form.cleaned_data.get('Q110'), numSousPartie=sp5)
                Q110.save()
                Q111 = Question(nomQuestion='Q111', reponseQuestion=form.cleaned_data.get('Q111'), numSousPartie=sp5)
                Q111.save()
                Q112 = Question(nomQuestion='Q112', reponseQuestion=form.cleaned_data.get('Q112'), numSousPartie=sp5)
                Q112.save()
                Q113 = Question(nomQuestion='Q113', reponseQuestion=form.cleaned_data.get('Q113'), numSousPartie=sp5)
                Q113.save()
                Q114 = Question(nomQuestion='Q114', reponseQuestion=form.cleaned_data.get('Q114'), numSousPartie=sp5)
                Q114.save()
                Q115 = Question(nomQuestion='Q115', reponseQuestion=form.cleaned_data.get('Q115'), numSousPartie=sp5)
                Q115.save()
                Q116 = Question(nomQuestion='Q116', reponseQuestion=form.cleaned_data.get('Q116'), numSousPartie=sp5)
                Q116.save()
                Q117 = Question(nomQuestion='Q117', reponseQuestion=form.cleaned_data.get('Q117'), numSousPartie=sp5)
                Q117.save()
                Q118 = Question(nomQuestion='Q118', reponseQuestion=form.cleaned_data.get('Q118'), numSousPartie=sp5)
                Q118.save()
                Q119 = Question(nomQuestion='Q119', reponseQuestion=form.cleaned_data.get('Q119'), numSousPartie=sp5)
                Q119.save()
                Q120 = Question(nomQuestion='Q120', reponseQuestion=form.cleaned_data.get('Q120'), numSousPartie=sp5)
                Q120.save()
                Q121 = Question(nomQuestion='Q121', reponseQuestion=form.cleaned_data.get('Q121'), numSousPartie=sp5)
                Q121.save()
                Q122 = Question(nomQuestion='Q122', reponseQuestion=form.cleaned_data.get('Q122'), numSousPartie=sp5)
                Q122.save()
                Q123 = Question(nomQuestion='Q123', reponseQuestion=form.cleaned_data.get('Q123'), numSousPartie=sp5)
                Q123.save()
                Q124 = Question(nomQuestion='Q124', reponseQuestion=form.cleaned_data.get('Q124'), numSousPartie=sp5)
                Q124.save()
                Q125 = Question(nomQuestion='Q125', reponseQuestion=form.cleaned_data.get('Q125'), numSousPartie=sp5)
                Q125.save()
                Q126 = Question(nomQuestion='Q126', reponseQuestion=form.cleaned_data.get('Q126'), numSousPartie=sp5)
                Q126.save()
                Q127 = Question(nomQuestion='Q127', reponseQuestion=form.cleaned_data.get('Q127'), numSousPartie=sp5)
                Q127.save()
                Q128 = Question(nomQuestion='Q128', reponseQuestion=form.cleaned_data.get('Q128'), numSousPartie=sp5)
                Q128.save()
                Q129 = Question(nomQuestion='Q129', reponseQuestion=form.cleaned_data.get('Q129'), numSousPartie=sp5)
                Q129.save()
                Q130 = Question(nomQuestion='Q130', reponseQuestion=form.cleaned_data.get('Q130'), numSousPartie=sp5)
                Q130.save()
                Q131 = Question(nomQuestion='Q131', reponseQuestion=form.cleaned_data.get('Q131'), numSousPartie=sp6)
                Q131.save()
                Q132 = Question(nomQuestion='Q132', reponseQuestion=form.cleaned_data.get('Q132'), numSousPartie=sp6)
                Q132.save()
                Q133 = Question(nomQuestion='Q133', reponseQuestion=form.cleaned_data.get('Q133'), numSousPartie=sp6)
                Q133.save()
                Q134 = Question(nomQuestion='Q134', reponseQuestion=form.cleaned_data.get('Q134'), numSousPartie=sp6)
                Q134.save()
                Q135 = Question(nomQuestion='Q135', reponseQuestion=form.cleaned_data.get('Q135'), numSousPartie=sp6)
                Q135.save()
                Q136 = Question(nomQuestion='Q136', reponseQuestion=form.cleaned_data.get('Q136'), numSousPartie=sp6)
                Q136.save()
                Q137 = Question(nomQuestion='Q137', reponseQuestion=form.cleaned_data.get('Q137'), numSousPartie=sp6)
                Q137.save()
                Q138 = Question(nomQuestion='Q138', reponseQuestion=form.cleaned_data.get('Q138'), numSousPartie=sp6)
                Q138.save()
                Q139 = Question(nomQuestion='Q139', reponseQuestion=form.cleaned_data.get('Q139'), numSousPartie=sp6)
                Q139.save()
                Q140 = Question(nomQuestion='Q140', reponseQuestion=form.cleaned_data.get('Q140'), numSousPartie=sp6)
                Q140.save()
                Q141 = Question(nomQuestion='Q141', reponseQuestion=form.cleaned_data.get('Q141'), numSousPartie=sp6)
                Q141.save()
                Q142 = Question(nomQuestion='Q142', reponseQuestion=form.cleaned_data.get('Q142'), numSousPartie=sp6)
                Q142.save()
                Q143 = Question(nomQuestion='Q143', reponseQuestion=form.cleaned_data.get('Q143'), numSousPartie=sp6)
                Q143.save()
                Q144 = Question(nomQuestion='Q144', reponseQuestion=form.cleaned_data.get('Q144'), numSousPartie=sp6)
                Q144.save()
                Q145 = Question(nomQuestion='Q145', reponseQuestion=form.cleaned_data.get('Q145'), numSousPartie=sp6)
                Q145.save()
                Q146 = Question(nomQuestion='Q146', reponseQuestion=form.cleaned_data.get('Q146'), numSousPartie=sp6)
                Q146.save()
                Q147 = Question(nomQuestion='Q147', reponseQuestion=form.cleaned_data.get('Q147'), numSousPartie=sp7)
                Q147.save()
                Q148 = Question(nomQuestion='Q148', reponseQuestion=form.cleaned_data.get('Q148'), numSousPartie=sp7)
                Q148.save()
                Q149 = Question(nomQuestion='Q149', reponseQuestion=form.cleaned_data.get('Q149'), numSousPartie=sp7)
                Q149.save()
                Q150 = Question(nomQuestion='Q150', reponseQuestion=form.cleaned_data.get('Q150'), numSousPartie=sp7)
                Q150.save()
                Q151 = Question(nomQuestion='Q151', reponseQuestion=form.cleaned_data.get('Q151'), numSousPartie=sp7)
                Q151.save()
                Q152 = Question(nomQuestion='Q152', reponseQuestion=form.cleaned_data.get('Q152'), numSousPartie=sp7)
                Q152.save()
                Q153 = Question(nomQuestion='Q153', reponseQuestion=form.cleaned_data.get('Q153'), numSousPartie=sp7)
                Q153.save()
                Q154 = Question(nomQuestion='Q154', reponseQuestion=form.cleaned_data.get('Q154'), numSousPartie=sp7)
                Q154.save()
                Q155 = Question(nomQuestion='Q155', reponseQuestion=form.cleaned_data.get('Q155'), numSousPartie=sp7)
                Q155.save()
                Q156 = Question(nomQuestion='Q156', reponseQuestion=form.cleaned_data.get('Q156'), numSousPartie=sp7)
                Q156.save()
                Q157 = Question(nomQuestion='Q157', reponseQuestion=form.cleaned_data.get('Q157'), numSousPartie=sp7)
                Q157.save()
                Q158 = Question(nomQuestion='Q158', reponseQuestion=form.cleaned_data.get('Q158'), numSousPartie=sp7)
                Q158.save()
                Q159 = Question(nomQuestion='Q159', reponseQuestion=form.cleaned_data.get('Q159'), numSousPartie=sp7)
                Q159.save()
                Q160 = Question(nomQuestion='Q160', reponseQuestion=form.cleaned_data.get('Q160'), numSousPartie=sp7)
                Q160.save()
                Q161 = Question(nomQuestion='Q161', reponseQuestion=form.cleaned_data.get('Q161'), numSousPartie=sp7)
                Q161.save()
                Q162 = Question(nomQuestion='Q162', reponseQuestion=form.cleaned_data.get('Q162'), numSousPartie=sp7)
                Q162.save()
                Q163 = Question(nomQuestion='Q163', reponseQuestion=form.cleaned_data.get('Q163'), numSousPartie=sp7)
                Q163.save()
                Q164 = Question(nomQuestion='Q164', reponseQuestion=form.cleaned_data.get('Q164'), numSousPartie=sp7)
                Q164.save()
                Q165 = Question(nomQuestion='Q165', reponseQuestion=form.cleaned_data.get('Q165'), numSousPartie=sp7)
                Q165.save()
                Q166 = Question(nomQuestion='Q166', reponseQuestion=form.cleaned_data.get('Q166'), numSousPartie=sp7)
                Q166.save()
                Q167 = Question(nomQuestion='Q167', reponseQuestion=form.cleaned_data.get('Q167'), numSousPartie=sp7)
                Q167.save()
                Q168 = Question(nomQuestion='Q168', reponseQuestion=form.cleaned_data.get('Q168'), numSousPartie=sp7)
                Q168.save()
                Q169 = Question(nomQuestion='Q169', reponseQuestion=form.cleaned_data.get('Q169'), numSousPartie=sp7)
                Q169.save()
                Q170 = Question(nomQuestion='Q170', reponseQuestion=form.cleaned_data.get('Q170'), numSousPartie=sp7)
                Q170.save()
                Q171 = Question(nomQuestion='Q171', reponseQuestion=form.cleaned_data.get('Q171'), numSousPartie=sp7)
                Q171.save()
                Q172 = Question(nomQuestion='Q172', reponseQuestion=form.cleaned_data.get('Q172'), numSousPartie=sp7)
                Q172.save()
                Q173 = Question(nomQuestion='Q173', reponseQuestion=form.cleaned_data.get('Q173'), numSousPartie=sp7)
                Q173.save()
                Q174 = Question(nomQuestion='Q174', reponseQuestion=form.cleaned_data.get('Q174'), numSousPartie=sp7)
                Q174.save()
                Q175 = Question(nomQuestion='Q175', reponseQuestion=form.cleaned_data.get('Q175'), numSousPartie=sp7)
                Q175.save()
                Q176 = Question(nomQuestion='Q176', reponseQuestion=form.cleaned_data.get('Q176'), numSousPartie=sp7)
                Q176.save()
                Q177 = Question(nomQuestion='Q177', reponseQuestion=form.cleaned_data.get('Q177'), numSousPartie=sp7)
                Q177.save()
                Q178 = Question(nomQuestion='Q178', reponseQuestion=form.cleaned_data.get('Q178'), numSousPartie=sp7)
                Q178.save()
                Q179 = Question(nomQuestion='Q179', reponseQuestion=form.cleaned_data.get('Q179'), numSousPartie=sp7)
                Q179.save()
                Q180 = Question(nomQuestion='Q180', reponseQuestion=form.cleaned_data.get('Q180'), numSousPartie=sp7)
                Q180.save()
                Q181 = Question(nomQuestion='Q181', reponseQuestion=form.cleaned_data.get('Q181'), numSousPartie=sp7)
                Q181.save()
                Q182 = Question(nomQuestion='Q182', reponseQuestion=form.cleaned_data.get('Q182'), numSousPartie=sp7)
                Q182.save()
                Q183 = Question(nomQuestion='Q183', reponseQuestion=form.cleaned_data.get('Q183'), numSousPartie=sp7)
                Q183.save()
                Q184 = Question(nomQuestion='Q184', reponseQuestion=form.cleaned_data.get('Q184'), numSousPartie=sp7)
                Q184.save()
                Q185 = Question(nomQuestion='Q185', reponseQuestion=form.cleaned_data.get('Q185'), numSousPartie=sp7)
                Q185.save()
                Q186 = Question(nomQuestion='Q186', reponseQuestion=form.cleaned_data.get('Q186'), numSousPartie=sp7)
                Q186.save()
                Q187 = Question(nomQuestion='Q187', reponseQuestion=form.cleaned_data.get('Q187'), numSousPartie=sp7)
                Q187.save()
                Q188 = Question(nomQuestion='Q188', reponseQuestion=form.cleaned_data.get('Q188'), numSousPartie=sp7)
                Q188.save()
                Q189 = Question(nomQuestion='Q189', reponseQuestion=form.cleaned_data.get('Q189'), numSousPartie=sp7)
                Q189.save()
                Q190 = Question(nomQuestion='Q190', reponseQuestion=form.cleaned_data.get('Q190'), numSousPartie=sp7)
                Q190.save()
                Q191 = Question(nomQuestion='Q191', reponseQuestion=form.cleaned_data.get('Q191'), numSousPartie=sp7)
                Q191.save()
                Q192 = Question(nomQuestion='Q192', reponseQuestion=form.cleaned_data.get('Q192'), numSousPartie=sp7)
                Q192.save()
                Q193 = Question(nomQuestion='Q193', reponseQuestion=form.cleaned_data.get('Q193'), numSousPartie=sp7)
                Q193.save()
                Q194 = Question(nomQuestion='Q194', reponseQuestion=form.cleaned_data.get('Q194'), numSousPartie=sp7)
                Q194.save()
                Q195 = Question(nomQuestion='Q195', reponseQuestion=form.cleaned_data.get('Q195'), numSousPartie=sp7)
                Q195.save()
                Q196 = Question(nomQuestion='Q196', reponseQuestion=form.cleaned_data.get('Q196'), numSousPartie=sp7)
                Q196.save()
                Q197 = Question(nomQuestion='Q197', reponseQuestion=form.cleaned_data.get('Q197'), numSousPartie=sp7)
                Q197.save()
                Q198 = Question(nomQuestion='Q198', reponseQuestion=form.cleaned_data.get('Q198'), numSousPartie=sp7)
                Q198.save()
                Q199 = Question(nomQuestion='Q199', reponseQuestion=form.cleaned_data.get('Q199'), numSousPartie=sp7)
                Q199.save()
                Q200 = Question(nomQuestion='Q200', reponseQuestion=form.cleaned_data.get('Q200'), numSousPartie=sp7)
                Q200.save()



                return read_subject(request,sub.numSujet)
        else:

            form = RemplirSujetForm()

        return render(request, 'create_subject.html', locals())


def read_subject_prof(request,idSujet):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        sub=Sujet.objects.get(numSujet=idSujet)
        return render (request, 'read_subject_prof.html', locals())

def read_subject(request,idSujet):
    sub = Sujet.objects.get(numSujet=idSujet)
    questions=[]
    parties = PartieSujet.objects.filter(numSujet=sub.numSujet)
    for part in parties:
        sp=SousPartie.objects.filter(numPartie=part.numPartie)
        for sousp in sp:
            quest = Question.objects.filter(numSousPartie=sousp.numSousPartie)
            for q in quest :
                questions.append(q)

    return render (request, 'read_subject.html', locals())

def create_subject_etu(request):
    if not request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        if request.method == 'POST':
            utilisateur = User.objects.get(id=request.user.id)

            form = ConnectionSubjectForm(request.POST)
            if form.is_valid():
                try :
                    sub = Sujet.objects.get(numSujet=form.cleaned_data["numSujet"],mdpSujet=form.cleaned_data["mdpSujet"])
                    return read_subject_etu(request, sub.numSujet)
                except :
                    return render(request, 'error_subject.html')
        else:
            form = ConnectionSubjectForm()
        return render(request, 'create_subject_prof.html', locals())

def read_subject_etu(request,idSujet):
    sub=Sujet.objects.get(numSujet=idSujet)
    return render (request, 'read_connexion_subject_etu.html', locals())

def make_subject_etu(request, idSujet):
    if not request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        if request.method == 'POST':
            etu = Etudiant.objects.get(numEtu=request.user.id)
            form = RemplirSujetForm(request.POST)

            if form.is_valid():

                subProf = Sujet.objects.get(numSujet=idSujet)

                sub = Sujet(nomSujet=subProf.nomSujet,mdpSujet=subProf.mdpSujet)
                sub.save()

                makeSub = FaireSujet(numSujet=sub, numEtu=etu)
                makeSub.save()

                corriger = Corriger(numSujetProf=subProf,numSujetEtu=sub)
                corriger.save()

                p1 = PartieSujet(nomPartie="Listening", dureePartie=50000, notePartie=0, numSujet=sub)
                p1.save()
                p2 = PartieSujet(nomPartie="Reading", dureePartie=50000, notePartie=0, numSujet=sub)
                p2.save()
                temps = p1.dureePartie + p2.dureePartie


                comp1 = Composer(numSujet=sub, numPartie=p1)
                comp1.save()
                comp2 = Composer(numSujet=sub, numPartie=p2)
                comp2.save()

                sp1 = SousPartie(nomSousPartie="Part 1", numPartie=p1)
                sp1.save()
                sp2 = SousPartie(nomSousPartie="Part 2", numPartie=p1)
                sp2.save()
                sp3 = SousPartie(nomSousPartie="Part 3", numPartie=p1)
                sp3.save()
                sp4 = SousPartie(nomSousPartie="Part 4", numPartie=p1)
                sp4.save()
                sp5 = SousPartie(nomSousPartie="Part 5", numPartie=p2)
                sp5.save()
                sp6 = SousPartie(nomSousPartie="Part 6", numPartie=p2)
                sp6.save()
                sp7 = SousPartie(nomSousPartie="Part 7", numPartie=p2)
                sp7.save()

                pos1 = Posseder(numSousPartie=sp1, numPartie=p1)
                pos1.save()
                pos2 = Posseder(numSousPartie=sp2, numPartie=p1)
                pos2.save()
                pos3 = Posseder(numSousPartie=sp3, numPartie=p1)
                pos3.save()
                pos4 = Posseder(numSousPartie=sp4, numPartie=p1)
                pos4.save()
                pos5 = Posseder(numSousPartie=sp5, numPartie=p2)
                pos5.save()
                pos6 = Posseder(numSousPartie=sp6, numPartie=p2)
                pos6.save()
                pos7 = Posseder(numSousPartie=sp7, numPartie=p2)
                pos7.save()

                Q1 = Question(nomQuestion='Q1', reponseQuestion=form.cleaned_data.get('Q1'), numSousPartie=sp1)
                Q1.save()
                Q2 = Question(nomQuestion='Q2', reponseQuestion=form.cleaned_data.get('Q2'), numSousPartie=sp1)
                Q2.save()
                Q3 = Question(nomQuestion='Q3', reponseQuestion=form.cleaned_data.get('Q3'), numSousPartie=sp1)
                Q3.save()
                Q4 = Question(nomQuestion='Q4', reponseQuestion=form.cleaned_data.get('Q4'), numSousPartie=sp1)
                Q4.save()
                Q5 = Question(nomQuestion='Q5', reponseQuestion=form.cleaned_data.get('Q5'), numSousPartie=sp1)
                Q5.save()
                Q6 = Question(nomQuestion='Q6', reponseQuestion=form.cleaned_data.get('Q6'), numSousPartie=sp1)
                Q6.save()
                Q7 = Question(nomQuestion='Q7', reponseQuestion=form.cleaned_data.get('Q7'), numSousPartie=sp2)
                Q7.save()
                Q8 = Question(nomQuestion='Q8', reponseQuestion=form.cleaned_data.get('Q8'), numSousPartie=sp2)
                Q8.save()
                Q9 = Question(nomQuestion='Q9', reponseQuestion=form.cleaned_data.get('Q9'), numSousPartie=sp2)
                Q9.save()
                Q10 = Question(nomQuestion='Q10', reponseQuestion=form.cleaned_data.get('Q10'), numSousPartie=sp2)
                Q10.save()
                Q11 = Question(nomQuestion='Q11', reponseQuestion=form.cleaned_data.get('Q11'), numSousPartie=sp2)
                Q11.save()
                Q12 = Question(nomQuestion='Q12', reponseQuestion=form.cleaned_data.get('Q12'), numSousPartie=sp2)
                Q12.save()
                Q13 = Question(nomQuestion='Q13', reponseQuestion=form.cleaned_data.get('Q13'), numSousPartie=sp2)
                Q13.save()
                Q14 = Question(nomQuestion='Q14', reponseQuestion=form.cleaned_data.get('Q14'), numSousPartie=sp2)
                Q14.save()
                Q15 = Question(nomQuestion='Q15', reponseQuestion=form.cleaned_data.get('Q15'), numSousPartie=sp2)
                Q15.save()
                Q16 = Question(nomQuestion='Q16', reponseQuestion=form.cleaned_data.get('Q16'), numSousPartie=sp2)
                Q16.save()
                Q17 = Question(nomQuestion='Q17', reponseQuestion=form.cleaned_data.get('Q17'), numSousPartie=sp2)
                Q17.save()
                Q18 = Question(nomQuestion='Q18', reponseQuestion=form.cleaned_data.get('Q18'), numSousPartie=sp2)
                Q18.save()
                Q19 = Question(nomQuestion='Q19', reponseQuestion=form.cleaned_data.get('Q19'), numSousPartie=sp2)
                Q19.save()
                Q20 = Question(nomQuestion='Q20', reponseQuestion=form.cleaned_data.get('Q20'), numSousPartie=sp2)
                Q20.save()
                Q21 = Question(nomQuestion='Q21', reponseQuestion=form.cleaned_data.get('Q21'), numSousPartie=sp2)
                Q21.save()
                Q22 = Question(nomQuestion='Q22', reponseQuestion=form.cleaned_data.get('Q22'), numSousPartie=sp2)
                Q22.save()
                Q23 = Question(nomQuestion='Q23', reponseQuestion=form.cleaned_data.get('Q23'), numSousPartie=sp2)
                Q23.save()
                Q24 = Question(nomQuestion='Q24', reponseQuestion=form.cleaned_data.get('Q24'), numSousPartie=sp2)
                Q24.save()
                Q25 = Question(nomQuestion='Q25', reponseQuestion=form.cleaned_data.get('Q25'), numSousPartie=sp2)
                Q25.save()
                Q26 = Question(nomQuestion='Q26', reponseQuestion=form.cleaned_data.get('Q26'), numSousPartie=sp2)
                Q26.save()
                Q27 = Question(nomQuestion='Q27', reponseQuestion=form.cleaned_data.get('Q27'), numSousPartie=sp2)
                Q27.save()
                Q28 = Question(nomQuestion='Q28', reponseQuestion=form.cleaned_data.get('Q28'), numSousPartie=sp2)
                Q28.save()
                Q29 = Question(nomQuestion='Q29', reponseQuestion=form.cleaned_data.get('Q29'), numSousPartie=sp2)
                Q29.save()
                Q30 = Question(nomQuestion='Q30', reponseQuestion=form.cleaned_data.get('Q30'), numSousPartie=sp2)
                Q30.save()
                Q31 = Question(nomQuestion='Q31', reponseQuestion=form.cleaned_data.get('Q31'), numSousPartie=sp2)
                Q31.save()
                Q32 = Question(nomQuestion='Q32', reponseQuestion=form.cleaned_data.get('Q32'), numSousPartie=sp3)
                Q32.save()
                Q33 = Question(nomQuestion='Q33', reponseQuestion=form.cleaned_data.get('Q33'), numSousPartie=sp3)
                Q33.save()
                Q34 = Question(nomQuestion='Q34', reponseQuestion=form.cleaned_data.get('Q34'), numSousPartie=sp3)
                Q34.save()
                Q35 = Question(nomQuestion='Q35', reponseQuestion=form.cleaned_data.get('Q35'), numSousPartie=sp3)
                Q35.save()
                Q36 = Question(nomQuestion='Q36', reponseQuestion=form.cleaned_data.get('Q36'), numSousPartie=sp3)
                Q36.save()
                Q37 = Question(nomQuestion='Q37', reponseQuestion=form.cleaned_data.get('Q37'), numSousPartie=sp3)
                Q37.save()
                Q38 = Question(nomQuestion='Q38', reponseQuestion=form.cleaned_data.get('Q38'), numSousPartie=sp3)
                Q38.save()
                Q39 = Question(nomQuestion='Q39', reponseQuestion=form.cleaned_data.get('Q39'), numSousPartie=sp3)
                Q39.save()
                Q40 = Question(nomQuestion='Q40', reponseQuestion=form.cleaned_data.get('Q40'), numSousPartie=sp3)
                Q40.save()
                Q41 = Question(nomQuestion='Q41', reponseQuestion=form.cleaned_data.get('Q41'), numSousPartie=sp3)
                Q41.save()
                Q42 = Question(nomQuestion='Q42', reponseQuestion=form.cleaned_data.get('Q42'), numSousPartie=sp3)
                Q42.save()
                Q43 = Question(nomQuestion='Q43', reponseQuestion=form.cleaned_data.get('Q43'), numSousPartie=sp3)
                Q43.save()
                Q44 = Question(nomQuestion='Q44', reponseQuestion=form.cleaned_data.get('Q44'), numSousPartie=sp3)
                Q44.save()
                Q45 = Question(nomQuestion='Q45', reponseQuestion=form.cleaned_data.get('Q45'), numSousPartie=sp3)
                Q45.save()
                Q46 = Question(nomQuestion='Q46', reponseQuestion=form.cleaned_data.get('Q46'), numSousPartie=sp3)
                Q46.save()
                Q47 = Question(nomQuestion='Q47', reponseQuestion=form.cleaned_data.get('Q47'), numSousPartie=sp3)
                Q47.save()
                Q48 = Question(nomQuestion='Q48', reponseQuestion=form.cleaned_data.get('Q48'), numSousPartie=sp3)
                Q48.save()
                Q49 = Question(nomQuestion='Q49', reponseQuestion=form.cleaned_data.get('Q49'), numSousPartie=sp3)
                Q49.save()
                Q50 = Question(nomQuestion='Q50', reponseQuestion=form.cleaned_data.get('Q50'), numSousPartie=sp3)
                Q50.save()
                Q51 = Question(nomQuestion='Q51', reponseQuestion=form.cleaned_data.get('Q51'), numSousPartie=sp3)
                Q51.save()
                Q52 = Question(nomQuestion='Q52', reponseQuestion=form.cleaned_data.get('Q52'), numSousPartie=sp3)
                Q52.save()
                Q53 = Question(nomQuestion='Q53', reponseQuestion=form.cleaned_data.get('Q53'), numSousPartie=sp3)
                Q53.save()
                Q54 = Question(nomQuestion='Q54', reponseQuestion=form.cleaned_data.get('Q54'), numSousPartie=sp3)
                Q54.save()
                Q55 = Question(nomQuestion='Q55', reponseQuestion=form.cleaned_data.get('Q55'), numSousPartie=sp3)
                Q55.save()
                Q56 = Question(nomQuestion='Q56', reponseQuestion=form.cleaned_data.get('Q56'), numSousPartie=sp3)
                Q56.save()
                Q57 = Question(nomQuestion='Q57', reponseQuestion=form.cleaned_data.get('Q57'), numSousPartie=sp3)
                Q57.save()
                Q58 = Question(nomQuestion='Q58', reponseQuestion=form.cleaned_data.get('Q58'), numSousPartie=sp3)
                Q58.save()
                Q59 = Question(nomQuestion='Q59', reponseQuestion=form.cleaned_data.get('Q59'), numSousPartie=sp3)
                Q59.save()
                Q60 = Question(nomQuestion='Q60', reponseQuestion=form.cleaned_data.get('Q60'), numSousPartie=sp3)
                Q60.save()
                Q61 = Question(nomQuestion='Q61', reponseQuestion=form.cleaned_data.get('Q61'), numSousPartie=sp3)
                Q61.save()
                Q62 = Question(nomQuestion='Q62', reponseQuestion=form.cleaned_data.get('Q62'), numSousPartie=sp3)
                Q62.save()
                Q63 = Question(nomQuestion='Q63', reponseQuestion=form.cleaned_data.get('Q63'), numSousPartie=sp3)
                Q63.save()
                Q64 = Question(nomQuestion='Q64', reponseQuestion=form.cleaned_data.get('Q64'), numSousPartie=sp3)
                Q64.save()
                Q65 = Question(nomQuestion='Q65', reponseQuestion=form.cleaned_data.get('Q65'), numSousPartie=sp3)
                Q65.save()
                Q66 = Question(nomQuestion='Q66', reponseQuestion=form.cleaned_data.get('Q66'), numSousPartie=sp3)
                Q66.save()
                Q67 = Question(nomQuestion='Q67', reponseQuestion=form.cleaned_data.get('Q67'), numSousPartie=sp3)
                Q67.save()
                Q68 = Question(nomQuestion='Q68', reponseQuestion=form.cleaned_data.get('Q68'), numSousPartie=sp3)
                Q68.save()
                Q69 = Question(nomQuestion='Q69', reponseQuestion=form.cleaned_data.get('Q69'), numSousPartie=sp3)
                Q69.save()
                Q70 = Question(nomQuestion='Q70', reponseQuestion=form.cleaned_data.get('Q70'), numSousPartie=sp3)
                Q70.save()
                Q71 = Question(nomQuestion='Q71', reponseQuestion=form.cleaned_data.get('Q71'), numSousPartie=sp4)
                Q71.save()
                Q72 = Question(nomQuestion='Q72', reponseQuestion=form.cleaned_data.get('Q72'), numSousPartie=sp4)
                Q72.save()
                Q73 = Question(nomQuestion='Q73', reponseQuestion=form.cleaned_data.get('Q73'), numSousPartie=sp4)
                Q73.save()
                Q74 = Question(nomQuestion='Q74', reponseQuestion=form.cleaned_data.get('Q74'), numSousPartie=sp4)
                Q74.save()
                Q75 = Question(nomQuestion='Q75', reponseQuestion=form.cleaned_data.get('Q75'), numSousPartie=sp4)
                Q75.save()
                Q76 = Question(nomQuestion='Q76', reponseQuestion=form.cleaned_data.get('Q76'), numSousPartie=sp4)
                Q76.save()
                Q77 = Question(nomQuestion='Q77', reponseQuestion=form.cleaned_data.get('Q77'), numSousPartie=sp4)
                Q77.save()
                Q78 = Question(nomQuestion='Q78', reponseQuestion=form.cleaned_data.get('Q78'), numSousPartie=sp4)
                Q78.save()
                Q79 = Question(nomQuestion='Q79', reponseQuestion=form.cleaned_data.get('Q79'), numSousPartie=sp4)
                Q79.save()
                Q80 = Question(nomQuestion='Q80', reponseQuestion=form.cleaned_data.get('Q80'), numSousPartie=sp4)
                Q80.save()
                Q81 = Question(nomQuestion='Q81', reponseQuestion=form.cleaned_data.get('Q81'), numSousPartie=sp4)
                Q81.save()
                Q82 = Question(nomQuestion='Q82', reponseQuestion=form.cleaned_data.get('Q82'), numSousPartie=sp4)
                Q82.save()
                Q83 = Question(nomQuestion='Q83', reponseQuestion=form.cleaned_data.get('Q83'), numSousPartie=sp4)
                Q83.save()
                Q84 = Question(nomQuestion='Q84', reponseQuestion=form.cleaned_data.get('Q84'), numSousPartie=sp4)
                Q84.save()
                Q85 = Question(nomQuestion='Q85', reponseQuestion=form.cleaned_data.get('Q85'), numSousPartie=sp4)
                Q85.save()
                Q86 = Question(nomQuestion='Q86', reponseQuestion=form.cleaned_data.get('Q86'), numSousPartie=sp4)
                Q86.save()
                Q87 = Question(nomQuestion='Q87', reponseQuestion=form.cleaned_data.get('Q87'), numSousPartie=sp4)
                Q87.save()
                Q88 = Question(nomQuestion='Q88', reponseQuestion=form.cleaned_data.get('Q88'), numSousPartie=sp4)
                Q88.save()
                Q89 = Question(nomQuestion='Q89', reponseQuestion=form.cleaned_data.get('Q89'), numSousPartie=sp4)
                Q89.save()
                Q90 = Question(nomQuestion='Q90', reponseQuestion=form.cleaned_data.get('Q90'), numSousPartie=sp4)
                Q90.save()
                Q91 = Question(nomQuestion='Q91', reponseQuestion=form.cleaned_data.get('Q91'), numSousPartie=sp4)
                Q91.save()
                Q92 = Question(nomQuestion='Q92', reponseQuestion=form.cleaned_data.get('Q92'), numSousPartie=sp4)
                Q92.save()
                Q93 = Question(nomQuestion='Q93', reponseQuestion=form.cleaned_data.get('Q93'), numSousPartie=sp4)
                Q93.save()
                Q94 = Question(nomQuestion='Q94', reponseQuestion=form.cleaned_data.get('Q94'), numSousPartie=sp4)
                Q94.save()
                Q95 = Question(nomQuestion='Q95', reponseQuestion=form.cleaned_data.get('Q95'), numSousPartie=sp4)
                Q95.save()
                Q96 = Question(nomQuestion='Q96', reponseQuestion=form.cleaned_data.get('Q96'), numSousPartie=sp4)
                Q96.save()
                Q97 = Question(nomQuestion='Q97', reponseQuestion=form.cleaned_data.get('Q97'), numSousPartie=sp4)
                Q97.save()
                Q98 = Question(nomQuestion='Q98', reponseQuestion=form.cleaned_data.get('Q98'), numSousPartie=sp4)
                Q98.save()
                Q99 = Question(nomQuestion='Q99', reponseQuestion=form.cleaned_data.get('Q99'), numSousPartie=sp4)
                Q99.save()
                Q100 = Question(nomQuestion='Q100', reponseQuestion=form.cleaned_data.get('Q100'), numSousPartie=sp4)
                Q100.save()
                Q101 = Question(nomQuestion='Q101', reponseQuestion=form.cleaned_data.get('Q101'), numSousPartie=sp5)
                Q101.save()
                Q102 = Question(nomQuestion='Q102', reponseQuestion=form.cleaned_data.get('Q102'), numSousPartie=sp5)
                Q102.save()
                Q103 = Question(nomQuestion='Q103', reponseQuestion=form.cleaned_data.get('Q103'), numSousPartie=sp5)
                Q103.save()
                Q104 = Question(nomQuestion='Q104', reponseQuestion=form.cleaned_data.get('Q104'), numSousPartie=sp5)
                Q104.save()
                Q105 = Question(nomQuestion='Q105', reponseQuestion=form.cleaned_data.get('Q105'), numSousPartie=sp5)
                Q105.save()
                Q106 = Question(nomQuestion='Q106', reponseQuestion=form.cleaned_data.get('Q106'), numSousPartie=sp5)
                Q106.save()
                Q107 = Question(nomQuestion='Q107', reponseQuestion=form.cleaned_data.get('Q107'), numSousPartie=sp5)
                Q107.save()
                Q108 = Question(nomQuestion='Q108', reponseQuestion=form.cleaned_data.get('Q108'), numSousPartie=sp5)
                Q108.save()
                Q109 = Question(nomQuestion='Q109', reponseQuestion=form.cleaned_data.get('Q109'), numSousPartie=sp5)
                Q109.save()
                Q110 = Question(nomQuestion='Q110', reponseQuestion=form.cleaned_data.get('Q110'), numSousPartie=sp5)
                Q110.save()
                Q111 = Question(nomQuestion='Q111', reponseQuestion=form.cleaned_data.get('Q111'), numSousPartie=sp5)
                Q111.save()
                Q112 = Question(nomQuestion='Q112', reponseQuestion=form.cleaned_data.get('Q112'), numSousPartie=sp5)
                Q112.save()
                Q113 = Question(nomQuestion='Q113', reponseQuestion=form.cleaned_data.get('Q113'), numSousPartie=sp5)
                Q113.save()
                Q114 = Question(nomQuestion='Q114', reponseQuestion=form.cleaned_data.get('Q114'), numSousPartie=sp5)
                Q114.save()
                Q115 = Question(nomQuestion='Q115', reponseQuestion=form.cleaned_data.get('Q115'), numSousPartie=sp5)
                Q115.save()
                Q116 = Question(nomQuestion='Q116', reponseQuestion=form.cleaned_data.get('Q116'), numSousPartie=sp5)
                Q116.save()
                Q117 = Question(nomQuestion='Q117', reponseQuestion=form.cleaned_data.get('Q117'), numSousPartie=sp5)
                Q117.save()
                Q118 = Question(nomQuestion='Q118', reponseQuestion=form.cleaned_data.get('Q118'), numSousPartie=sp5)
                Q118.save()
                Q119 = Question(nomQuestion='Q119', reponseQuestion=form.cleaned_data.get('Q119'), numSousPartie=sp5)
                Q119.save()
                Q120 = Question(nomQuestion='Q120', reponseQuestion=form.cleaned_data.get('Q120'), numSousPartie=sp5)
                Q120.save()
                Q121 = Question(nomQuestion='Q121', reponseQuestion=form.cleaned_data.get('Q121'), numSousPartie=sp5)
                Q121.save()
                Q122 = Question(nomQuestion='Q122', reponseQuestion=form.cleaned_data.get('Q122'), numSousPartie=sp5)
                Q122.save()
                Q123 = Question(nomQuestion='Q123', reponseQuestion=form.cleaned_data.get('Q123'), numSousPartie=sp5)
                Q123.save()
                Q124 = Question(nomQuestion='Q124', reponseQuestion=form.cleaned_data.get('Q124'), numSousPartie=sp5)
                Q124.save()
                Q125 = Question(nomQuestion='Q125', reponseQuestion=form.cleaned_data.get('Q125'), numSousPartie=sp5)
                Q125.save()
                Q126 = Question(nomQuestion='Q126', reponseQuestion=form.cleaned_data.get('Q126'), numSousPartie=sp5)
                Q126.save()
                Q127 = Question(nomQuestion='Q127', reponseQuestion=form.cleaned_data.get('Q127'), numSousPartie=sp5)
                Q127.save()
                Q128 = Question(nomQuestion='Q128', reponseQuestion=form.cleaned_data.get('Q128'), numSousPartie=sp5)
                Q128.save()
                Q129 = Question(nomQuestion='Q129', reponseQuestion=form.cleaned_data.get('Q129'), numSousPartie=sp5)
                Q129.save()
                Q130 = Question(nomQuestion='Q130', reponseQuestion=form.cleaned_data.get('Q130'), numSousPartie=sp5)
                Q130.save()
                Q131 = Question(nomQuestion='Q131', reponseQuestion=form.cleaned_data.get('Q131'), numSousPartie=sp6)
                Q131.save()
                Q132 = Question(nomQuestion='Q132', reponseQuestion=form.cleaned_data.get('Q132'), numSousPartie=sp6)
                Q132.save()
                Q133 = Question(nomQuestion='Q133', reponseQuestion=form.cleaned_data.get('Q133'), numSousPartie=sp6)
                Q133.save()
                Q134 = Question(nomQuestion='Q134', reponseQuestion=form.cleaned_data.get('Q134'), numSousPartie=sp6)
                Q134.save()
                Q135 = Question(nomQuestion='Q135', reponseQuestion=form.cleaned_data.get('Q135'), numSousPartie=sp6)
                Q135.save()
                Q136 = Question(nomQuestion='Q136', reponseQuestion=form.cleaned_data.get('Q136'), numSousPartie=sp6)
                Q136.save()
                Q137 = Question(nomQuestion='Q137', reponseQuestion=form.cleaned_data.get('Q137'), numSousPartie=sp6)
                Q137.save()
                Q138 = Question(nomQuestion='Q138', reponseQuestion=form.cleaned_data.get('Q138'), numSousPartie=sp6)
                Q138.save()
                Q139 = Question(nomQuestion='Q139', reponseQuestion=form.cleaned_data.get('Q139'), numSousPartie=sp6)
                Q139.save()
                Q140 = Question(nomQuestion='Q140', reponseQuestion=form.cleaned_data.get('Q140'), numSousPartie=sp6)
                Q140.save()
                Q141 = Question(nomQuestion='Q141', reponseQuestion=form.cleaned_data.get('Q141'), numSousPartie=sp6)
                Q141.save()
                Q142 = Question(nomQuestion='Q142', reponseQuestion=form.cleaned_data.get('Q142'), numSousPartie=sp6)
                Q142.save()
                Q143 = Question(nomQuestion='Q143', reponseQuestion=form.cleaned_data.get('Q143'), numSousPartie=sp6)
                Q143.save()
                Q144 = Question(nomQuestion='Q144', reponseQuestion=form.cleaned_data.get('Q144'), numSousPartie=sp6)
                Q144.save()
                Q145 = Question(nomQuestion='Q145', reponseQuestion=form.cleaned_data.get('Q145'), numSousPartie=sp6)
                Q145.save()
                Q146 = Question(nomQuestion='Q146', reponseQuestion=form.cleaned_data.get('Q146'), numSousPartie=sp6)
                Q146.save()
                Q147 = Question(nomQuestion='Q147', reponseQuestion=form.cleaned_data.get('Q147'), numSousPartie=sp7)
                Q147.save()
                Q148 = Question(nomQuestion='Q148', reponseQuestion=form.cleaned_data.get('Q148'), numSousPartie=sp7)
                Q148.save()
                Q149 = Question(nomQuestion='Q149', reponseQuestion=form.cleaned_data.get('Q149'), numSousPartie=sp7)
                Q149.save()
                Q150 = Question(nomQuestion='Q150', reponseQuestion=form.cleaned_data.get('Q150'), numSousPartie=sp7)
                Q150.save()
                Q151 = Question(nomQuestion='Q151', reponseQuestion=form.cleaned_data.get('Q151'), numSousPartie=sp7)
                Q151.save()
                Q152 = Question(nomQuestion='Q152', reponseQuestion=form.cleaned_data.get('Q152'), numSousPartie=sp7)
                Q152.save()
                Q153 = Question(nomQuestion='Q153', reponseQuestion=form.cleaned_data.get('Q153'), numSousPartie=sp7)
                Q153.save()
                Q154 = Question(nomQuestion='Q154', reponseQuestion=form.cleaned_data.get('Q154'), numSousPartie=sp7)
                Q154.save()
                Q155 = Question(nomQuestion='Q155', reponseQuestion=form.cleaned_data.get('Q155'), numSousPartie=sp7)
                Q155.save()
                Q156 = Question(nomQuestion='Q156', reponseQuestion=form.cleaned_data.get('Q156'), numSousPartie=sp7)
                Q156.save()
                Q157 = Question(nomQuestion='Q157', reponseQuestion=form.cleaned_data.get('Q157'), numSousPartie=sp7)
                Q157.save()
                Q158 = Question(nomQuestion='Q158', reponseQuestion=form.cleaned_data.get('Q158'), numSousPartie=sp7)
                Q158.save()
                Q159 = Question(nomQuestion='Q159', reponseQuestion=form.cleaned_data.get('Q159'), numSousPartie=sp7)
                Q159.save()
                Q160 = Question(nomQuestion='Q160', reponseQuestion=form.cleaned_data.get('Q160'), numSousPartie=sp7)
                Q160.save()
                Q161 = Question(nomQuestion='Q161', reponseQuestion=form.cleaned_data.get('Q161'), numSousPartie=sp7)
                Q161.save()
                Q162 = Question(nomQuestion='Q162', reponseQuestion=form.cleaned_data.get('Q162'), numSousPartie=sp7)
                Q162.save()
                Q163 = Question(nomQuestion='Q163', reponseQuestion=form.cleaned_data.get('Q163'), numSousPartie=sp7)
                Q163.save()
                Q164 = Question(nomQuestion='Q164', reponseQuestion=form.cleaned_data.get('Q164'), numSousPartie=sp7)
                Q164.save()
                Q165 = Question(nomQuestion='Q165', reponseQuestion=form.cleaned_data.get('Q165'), numSousPartie=sp7)
                Q165.save()
                Q166 = Question(nomQuestion='Q166', reponseQuestion=form.cleaned_data.get('Q166'), numSousPartie=sp7)
                Q166.save()
                Q167 = Question(nomQuestion='Q167', reponseQuestion=form.cleaned_data.get('Q167'), numSousPartie=sp7)
                Q167.save()
                Q168 = Question(nomQuestion='Q168', reponseQuestion=form.cleaned_data.get('Q168'), numSousPartie=sp7)
                Q168.save()
                Q169 = Question(nomQuestion='Q169', reponseQuestion=form.cleaned_data.get('Q169'), numSousPartie=sp7)
                Q169.save()
                Q170 = Question(nomQuestion='Q170', reponseQuestion=form.cleaned_data.get('Q170'), numSousPartie=sp7)
                Q170.save()
                Q171 = Question(nomQuestion='Q171', reponseQuestion=form.cleaned_data.get('Q171'), numSousPartie=sp7)
                Q171.save()
                Q172 = Question(nomQuestion='Q172', reponseQuestion=form.cleaned_data.get('Q172'), numSousPartie=sp7)
                Q172.save()
                Q173 = Question(nomQuestion='Q173', reponseQuestion=form.cleaned_data.get('Q173'), numSousPartie=sp7)
                Q173.save()
                Q174 = Question(nomQuestion='Q174', reponseQuestion=form.cleaned_data.get('Q174'), numSousPartie=sp7)
                Q174.save()
                Q175 = Question(nomQuestion='Q175', reponseQuestion=form.cleaned_data.get('Q175'), numSousPartie=sp7)
                Q175.save()
                Q176 = Question(nomQuestion='Q176', reponseQuestion=form.cleaned_data.get('Q176'), numSousPartie=sp7)
                Q176.save()
                Q177 = Question(nomQuestion='Q177', reponseQuestion=form.cleaned_data.get('Q177'), numSousPartie=sp7)
                Q177.save()
                Q178 = Question(nomQuestion='Q178', reponseQuestion=form.cleaned_data.get('Q178'), numSousPartie=sp7)
                Q178.save()
                Q179 = Question(nomQuestion='Q179', reponseQuestion=form.cleaned_data.get('Q179'), numSousPartie=sp7)
                Q179.save()
                Q180 = Question(nomQuestion='Q180', reponseQuestion=form.cleaned_data.get('Q180'), numSousPartie=sp7)
                Q180.save()
                Q181 = Question(nomQuestion='Q181', reponseQuestion=form.cleaned_data.get('Q181'), numSousPartie=sp7)
                Q181.save()
                Q182 = Question(nomQuestion='Q182', reponseQuestion=form.cleaned_data.get('Q182'), numSousPartie=sp7)
                Q182.save()
                Q183 = Question(nomQuestion='Q183', reponseQuestion=form.cleaned_data.get('Q183'), numSousPartie=sp7)
                Q183.save()
                Q184 = Question(nomQuestion='Q184', reponseQuestion=form.cleaned_data.get('Q184'), numSousPartie=sp7)
                Q184.save()
                Q185 = Question(nomQuestion='Q185', reponseQuestion=form.cleaned_data.get('Q185'), numSousPartie=sp7)
                Q185.save()
                Q186 = Question(nomQuestion='Q186', reponseQuestion=form.cleaned_data.get('Q186'), numSousPartie=sp7)
                Q186.save()
                Q187 = Question(nomQuestion='Q187', reponseQuestion=form.cleaned_data.get('Q187'), numSousPartie=sp7)
                Q187.save()
                Q188 = Question(nomQuestion='Q188', reponseQuestion=form.cleaned_data.get('Q188'), numSousPartie=sp7)
                Q188.save()
                Q189 = Question(nomQuestion='Q189', reponseQuestion=form.cleaned_data.get('Q189'), numSousPartie=sp7)
                Q189.save()
                Q190 = Question(nomQuestion='Q190', reponseQuestion=form.cleaned_data.get('Q190'), numSousPartie=sp7)
                Q190.save()
                Q191 = Question(nomQuestion='Q191', reponseQuestion=form.cleaned_data.get('Q191'), numSousPartie=sp7)
                Q191.save()
                Q192 = Question(nomQuestion='Q192', reponseQuestion=form.cleaned_data.get('Q192'), numSousPartie=sp7)
                Q192.save()
                Q193 = Question(nomQuestion='Q193', reponseQuestion=form.cleaned_data.get('Q193'), numSousPartie=sp7)
                Q193.save()
                Q194 = Question(nomQuestion='Q194', reponseQuestion=form.cleaned_data.get('Q194'), numSousPartie=sp7)
                Q194.save()
                Q195 = Question(nomQuestion='Q195', reponseQuestion=form.cleaned_data.get('Q195'), numSousPartie=sp7)
                Q195.save()
                Q196 = Question(nomQuestion='Q196', reponseQuestion=form.cleaned_data.get('Q196'), numSousPartie=sp7)
                Q196.save()
                Q197 = Question(nomQuestion='Q197', reponseQuestion=form.cleaned_data.get('Q197'), numSousPartie=sp7)
                Q197.save()
                Q198 = Question(nomQuestion='Q198', reponseQuestion=form.cleaned_data.get('Q198'), numSousPartie=sp7)
                Q198.save()
                Q199 = Question(nomQuestion='Q199', reponseQuestion=form.cleaned_data.get('Q199'), numSousPartie=sp7)
                Q199.save()
                Q200 = Question(nomQuestion='Q200', reponseQuestion=form.cleaned_data.get('Q200'), numSousPartie=sp7)
                Q200.save()

                return read_subject(request, sub.numSujet)
        else:

            form = RemplirSujetForm()



        return render(request, 'create_subject.html', locals())

@login_required
def read_mySubject(request,idSujet):
    sujets = FaireSujet.objects.filter(numSujet=idSujet)
    sub = []
    for suj in sujets:
        sub+=suj.numSujet

    return render(request, 'read_mySubject.html', locals())

def corriger_sujet(request,idSujet):
    subEtu = Sujet.objects.get(numSujet=idSujet)
    subs=Corriger.objects.get(numSujetEtu=subEtu)
    subProf=subs.numSujetProf

    note = 0
    listening = 0
    reading = 0

    partieProf = PartieSujet.objects.filter(numSujet=subProf)
    listProf = partieProf[0]
    readProf = partieProf[1]
    print(listProf)
    print(readProf)
    sp1Prof = SousPartie.objects.get(numPartie=listProf.numPartie, nomSousPartie="Part 1")
    sp2Prof = SousPartie.objects.get(numPartie=listProf.numPartie, nomSousPartie="Part 2")
    sp3Prof = SousPartie.objects.get(numPartie=listProf.numPartie, nomSousPartie="Part 3")
    sp4Prof = SousPartie.objects.get(numPartie=listProf.numPartie, nomSousPartie="Part 4")
    sp5Prof = SousPartie.objects.get(numPartie=readProf.numPartie,nomSousPartie="Part 5")
    print(sp5Prof)
    sp6Prof = SousPartie.objects.get(numPartie=readProf.numPartie, nomSousPartie="Part 6")
    sp7Prof = SousPartie.objects.get(numPartie=readProf.numPartie, nomSousPartie="Part 7")

    listProf=[]
    readProf=[]
    QuestP1 = Question.objects.filter(numSousPartie=sp1Prof)
    for quest in QuestP1:
        listProf += [quest]

    QuestP2 = Question.objects.filter(numSousPartie=sp2Prof)
    for quest in QuestP2:
        listProf += [quest]
    QuestP3 = Question.objects.filter(numSousPartie=sp3Prof)
    for quest in QuestP3:
        listProf += [quest]
    QuestP4 = Question.objects.filter(numSousPartie=sp4Prof)
    for quest in QuestP4:
        listProf += [quest]

    QuestP5 = Question.objects.filter(numSousPartie=sp5Prof)
    for quest in QuestP5:
        readProf += [quest]
    QuestP6 = Question.objects.filter(numSousPartie=sp6Prof)
    for quest in QuestP6:
        readProf += [quest]
    QuestP7 = Question.objects.filter(numSousPartie=sp7Prof)
    for quest in QuestP7:
        readProf += [quest]

    partieEtu = PartieSujet.objects.filter(numSujet=subEtu.numSujet)
    listEtu = partieEtu[0]
    readEtu = partieEtu[1]
    print(listEtu)
    print(readEtu)

    sp1Etu = SousPartie.objects.filter(numPartie=listEtu.numPartie, nomSousPartie="Part 1")
    print(sp1Etu)
    sp2Etu = SousPartie.objects.filter(numPartie=listEtu.numPartie, nomSousPartie="Part 2")
    sp3Etu = SousPartie.objects.filter(numPartie=listEtu.numPartie, nomSousPartie="Part 3")
    sp4Etu = SousPartie.objects.filter(numPartie=listEtu.numPartie, nomSousPartie="Part 4")
    sp5Etu = SousPartie.objects.filter(numPartie=readEtu.numPartie, nomSousPartie="Part 5")
    sp6Etu = SousPartie.objects.filter(numPartie=readEtu.numPartie, nomSousPartie="Part 6")
    sp7Etu = SousPartie.objects.filter(numPartie=readEtu.numPartie, nomSousPartie="Part 7")

    listEtu = []
    readEtu = []


    QuestP1 = Question.objects.filter(numSousPartie=sp1Etu[0])
    print(QuestP1)
    for quest in QuestP1:
        listEtu += [quest]

    QuestP2 = Question.objects.filter(numSousPartie=sp2Etu[0])
    for quest in QuestP2:
        listEtu += [quest]
    QuestP3 = Question.objects.filter(numSousPartie=sp3Etu[0])
    for quest in QuestP3:
        listEtu += [quest]
    QuestP4 = Question.objects.filter(numSousPartie=sp4Etu[0])
    for quest in QuestP4:
        listEtu += [quest]

    QuestP5 = Question.objects.filter(numSousPartie=sp5Etu[0])
    for quest in QuestP5:
        readEtu += [quest]
    QuestP6 = Question.objects.filter(numSousPartie=sp6Etu[0])
    for quest in QuestP6:
        readEtu += [quest]
    QuestP7 = Question.objects.filter(numSousPartie=sp7Etu[0])
    for quest in QuestP7:
        readEtu += [quest]

    for i in range (0,100):
        if listEtu[i].reponseQuestion == listProf[i].reponseQuestion:
            listening +=1

    for i in range (0,100):
        if readEtu[i].reponseQuestion == readProf[i].reponseQuestion:
            reading +=1


    #conversion des notes:
    noteListening=[0,5,5,5,5,5,5,5,5,5,5,
                   5,5,5,5,5,5,10,15,20,25,
                   30,35,40,45,50,55,60,70,80,85,
                   90,95,100,105,115,125,135,140,150,160,
                   170,175,180,190,200,205,215,220,225,230,
                   235,245,255,260,265,275,285,290,295,300,
                   310,320,325,330,335,340,345,350,355,360,
                   365,370,375,385,395,400,405,415,420,425,
                   430,435,440,445,450,455,460,465,475,480,
                   485,490,495,495,495,495,495,495,495,495]
    noteReading=[0,5,5,5,5,5,5,5,5,5,5,
                 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                 10,15,20,25,30,35,40,45,55,60,
                 65,70,75,80,85,90,95,105,115,120,
                 125,130,135,140,145,155,160,170,175,185,
                 195,205,210,215,220,230,240,245,250,255,
                 260,270,275,280,285,290,295,295,300,310,
                 315,320,325,330,335,340,345,355,360,370,
                 375,385,390,395,400,405,415,420,425,435,
                 440,450,455,460,470,475,485,485,490,495]

    listeningEtu = PartieSujet.objects.get(numPartie = partieEtu[0].numPartie)
    listeningEtu.notePartie = noteListening[listening]
    listeningEtu.save()
    readingEtu = PartieSujet.objects.get(numPartie = partieEtu[1].numPartie)
    readingEtu.notePartie = noteReading[reading]
    readingEtu.save()

    note = noteListening[listening] + noteReading[reading]

    return render(request, 'corriger_sujet.html', locals())


@login_required
def create_session(request):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        prof = Professeur.objects.get(numProf=request.user.id)
        if request.method == 'POST':

            form = CreateSessionForm(request.POST)
            if form.is_valid():

                    sub = Sujet.objects.get(numSujet=form.cleaned_data["numSujet"])


                    sess = SessionToeic(dateSession=form.cleaned_data["dateSession"])
                    sess.save()
                    corresp = Correspondre(numSujet=sub,numSession=sess)
                    corresp.save()


                    return read_session(request,sess)

        else:
            form = CreateSessionForm()
        return render(request, 'create_session_prof.html', locals())

@login_required
def read_session(request,idSession):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        sess = SessionToeic.objects.get(numSession=idSession.numSession)
        cor = Correspondre.objects.get(numSession=sess)

        return render(request, 'read_session.html', locals())

@login_required
def lire_sujets(request):
    listSujetProf = []
    listSujetEtu = []
    if request.session['estEtu']:
            userEtu = Etudiant.objects.get(numEtu=request.user.id)

            liste = FaireSujet.objects.filter(numEtu=userEtu)



            for i in liste :
                listSujetEtu.append(i.numSujet)

                try:
                    sujetProf = Corriger.objects.get(numSujetEtu=i.numSujet)
                    listSujetProf.append(sujetProf)
                except:
                    listSujetProf



    return render(request, 'listeSujet.html', locals())

@login_required
def updateEtu(request):
    if not request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        user = User.objects.get(id=request.user.id)
        etu = Etudiant.objects.get(numEtu=request.user.id)
        if request.method == "POST":
            form = UpdateFormEtu(request.POST)

            if form.is_valid():
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.save()
                try:
                     classe = Classe.objects.get(nomClasse= form.cleaned_data.get('classeEtu'))
                except:
                    classe = Classe(nomClasse=form.cleaned_data.get('classeEtu'), promoClasse=form.cleaned_data.get('promoEtu'))
                    classe.save()
                etu.classeEtu = classe
                etu.promoEtu = form.cleaned_data.get('promoEtu')
                etu.save()
                return monCompte_etu(request)
        else:
            form = UpdateFormEtu()
            Classe_choices = ['IG3','IG4', 'IG5','MAT3', 'MAT4', 'MAT5', 'PEIP1', 'PEIP2', 'GBA3', 'GBA4', 'GBA5', 'MI3', 'MI4', 'MI5','STE3', 'STE4', 'STE5'
            ]
        return render(request, 'updateEtu.html', locals())

@login_required
def updateProf(request):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        user = User.objects.get(id=request.user.id)
        prof = Professeur.objects.get(numProf=request.user.id)
        if request.method == "POST":
            form = UpdateFormProf(request.POST)
            if form.is_valid():
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.save()
                return monCompte_prof(request)
        else:
            form = UpdateFormProf()
        return render(request, 'updateProf.html', locals())


#permet de delete un etudiant
@login_required
def delete_etu(request):
    user = User.objects.get(id=request.user.id)
    etu = Etudiant.objects.get(numEtu=request.user.id)
    if request.method == 'POST':
        User.objects.get(id=request.user.id).delete()
        Etudiant.objects.get(numEtu=request.user.id).delete()
        return render(request, 'index.html')

    return render(request, 'deleteEtu.html')

@login_required
def stats_par_sujet_etu(request):
    if not request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        userEtu = Etudiant.objects.get(numEtu=request.user.id)
        parties = []
        notes = []
        liste = FaireSujet.objects.filter(numEtu=userEtu)
        listeNumSujets = []
        for b in liste:
            listeNumSujets.append(b.numSujet)
#listeNumSujets contient tous les numéros de sujets fait par l'eleve
        for i in listeNumSujets :
            partie = PartieSujet.objects.filter(numSujet= i)
            # partie contient les parties sujets 
            for j in partie : 
                parties.append(j)
# parties contient toutes les parties d'un élève 
        return render(request, 'stats_par_sujet_etu.html', locals())




@login_required
def stats_par_sujet_prof(request,idSujet):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        corr = Corriger.objects.filter(numSujetProf = idSujet)
        for l in corr : 

            partieReading = PartieSujet.objects.filter(numSujet= l.numSujetEtu,nomPartie = "Reading")
            partieListening = PartieSujet.objects.filter(numSujet= l.numSujetEtu,nomPartie = "Listening")
            listeReading = []
            listeListening = []
            listeFinale = []

            for i in partieReading :
                listeReading.append(i.notePartie)
                

            for j in partieListening :
                listeListening.append(j.notePartie)
                
            for k in range(0,len(listeListening)):
                listeFinale.append(listeListening[k] + listeReading[k])

        
        moyenne = numpy.mean(listeFinale)
        minimum = numpy.amin(listeFinale)
        maximum = numpy.amax(listeFinale)


        return render(request, 'stats_par_sujet_prof.html', locals())

@login_required
def liste_sujet_prof(request,):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else :
        requeteSujet = Proposer.objects.filter(numProf= request.user.id)
        listeSujet = []
        for i in requeteSujet :
            listeSujet.append(i)

    return render(request, 'liste_sujet_prof.html', locals())


@login_required
def stats_par_partie_prof(request):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        listeSujet = []
        f = FaireSujet.objects.all()
        for i in f :
            listeSujet.append(i.numSujet)

        
        parties = []
        notesListening = []
        notesReading = []
        parties = PartieSujet.objects.filter(numSujet__in=listeSujet)
        for i in parties :
                if (i.nomPartie == "Reading") :
                    notesReading.append(i.notePartie)
                else :
                    notesListening.append(i.notePartie)

        moyListening = numpy.mean(notesListening)
        moyReading = numpy.mean(notesReading)
        maxReading = numpy.amax(notesReading)
        minReading = numpy.amin(notesReading)
        maxListening = numpy.amax(notesListening)
        minListening = numpy.amin(notesListening)
        
        return render(request, 'stats_par_partie_prof.html', locals())

@login_required
def stats_par_sujet_prof(request,idSujet):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else:
        partieReading = PartieSujet.objects.filter(numSujet= idSujet)
        partieListening = PartieSujet.objects.filter(numSujet= idSujet,nomPartie = "Listening")
        listeReading = []
        listeListening = []
        listeFinale = []

        for i in partieReading :
            listeReading.append(i.notePartie)
            

        for j in partieListening :
            listeListening.append(j.notePartie)
            
        for k in range(0,len(listeListening)):
            listeFinale.append(listeListening[k] + listeReading[k])

        
        moyenne = numpy.mean(listeFinale)
        minimum = numpy.amin(listeFinale)
        maximum = numpy.amax(listeFinale)


        return render(request, 'stats_par_sujet_prof.html', locals())

@login_required
def liste_sujet_prof(request,):
    if request.session['estEtu']:
        return render(request, 'error404.html')
    else :
        listeSujet = Corriger.objects.all()





    return render(request, 'liste_sujet_prof.html', locals())