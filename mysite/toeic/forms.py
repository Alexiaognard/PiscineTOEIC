from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from toeic.models import *


#Formulaire pour la connexion au site
class SignInForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

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

#Formulaire de creation d'un compte étudiant
class SignUpFormEtu(UserCreationForm):
    classeEtu = forms.ChoiceField(label="Class",choices=Classe_choices)
    promoEtu = forms.IntegerField(label="Prom")
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','classeEtu','promoEtu','password1', 'password2' )

#Formulaire de creation d'un compte professeur
class SignUpFormProf(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1', 'password2' )


#formulaire de création d'un sujet
class CreateSubjectForm(forms.Form):
    nomSujet = forms.CharField(label="Name")
    mdpSujet = forms.CharField(label="Password")
    class Meta:
        model = Sujet
        fields = ('nomSujet','mdpSujet')

#formulaire de création d'un sujet
class ConnectionSubjectForm(forms.Form):
    numSujet = forms.CharField(label="Num")
    mdpSujet = forms.CharField(label="Password")
    class Meta:
        model = Sujet
        fields = ('numSujet','mdpSujet')

class CreateSessionForm(forms.Form):
    dateSession = forms.DateTimeField(label="Day")
    numSujet = forms.IntegerField(label="num Subject")
    class Meta:
        model = SessionToeic
        fields = ("dateSession", "numSujet")



QUESTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D','D'),
    ]





class RemplirSujetForm(forms.Form):

    Q1 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q2 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q3 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q4 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q5 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q6 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q7 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q8 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q9 = forms.ChoiceField(choices=QUESTION_CHOICES)

    Q10 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q11 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q12 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q13 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q14 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q15 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q16 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q17 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q18 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q19 = forms.ChoiceField(choices=QUESTION_CHOICES)

    Q20 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q21 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q22 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q23 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q24 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q25 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q26 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q27 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q28 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q29 = forms.ChoiceField(choices=QUESTION_CHOICES)

    Q30 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q31 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q32 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q33 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q34 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q35 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q36 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q37 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q38 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q39 = forms.ChoiceField(choices=QUESTION_CHOICES)

    Q40 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q41 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q42 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q43 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q44 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q45 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q46 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q47 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q48 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q49 = forms.ChoiceField(choices=QUESTION_CHOICES)

    Q50 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q51 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q52 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q53 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q54 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q55 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q56 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q57 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q58 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q59 = forms.ChoiceField(choices=QUESTION_CHOICES)

    Q60 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q61 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q62 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q63 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q64 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q65 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q66 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q67 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q68 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q69 = forms.ChoiceField(choices=QUESTION_CHOICES)

    Q70 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q71 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q72 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q73 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q74 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q75 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q76 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q77 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q78 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q79 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q80 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q81 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q82 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q83 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q84 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q85 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q86 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q87 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q88 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q89 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q90 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q91 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q92 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q93 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q94 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q95 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q96 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q97 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q98 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q99 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q100 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q101 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q102 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q103 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q104 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q105 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q106 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q107 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q108 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q109 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q110 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q111 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q112 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q113 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q114 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q115 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q116 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q117 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q118 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q119 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q120 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q121 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q122 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q123 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q124 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q125 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q126 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q127 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q128 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q129 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q130 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q131 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q132 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q133 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q134 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q135 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q136 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q137 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q138 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q139 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q140 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q141 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q142 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q143 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q144 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q145 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q146 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q147 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q148 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q149 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q150 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q151 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q152 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q153 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q154 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q155 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q156 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q157 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q158 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q159 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q160 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q161 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q162 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q163 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q164 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q165 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q166 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q167 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q168 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q169 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q170 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q171 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q172 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q173 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q174 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q175 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q176 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q177 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q178 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q179 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q180 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q181 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q182 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q183 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q184 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q185 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q186 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q187 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q188 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q189 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q190 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q191 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q192 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q193 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q194 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q195 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q196 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q197 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q198 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q199 = forms.ChoiceField(choices=QUESTION_CHOICES)
    Q200 = forms.ChoiceField(choices=QUESTION_CHOICES)
    class Meta:
        model = Question
        fields = "__all__"
