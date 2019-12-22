from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from toeic.models import *


#Formulaire pour la connexion au site
class SignInForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


#Formulaire de creation d'un compte étudiant
class SignUpFormEtu(UserCreationForm):
    classeEtu = forms.CharField(label="Classe")
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','classeEtu','password1', 'password2' )


