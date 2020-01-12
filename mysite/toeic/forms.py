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
        ('MI5', 'MI5'),
        ('STE3','STE3'),
        ('STE4', 'STE4'),
        ('STE5','STE5')
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
    Q1 = forms.CharField(label='Q1')
    Q2 = forms.CharField(label='Q2')
    Q3 = forms.CharField(label='Q3')
    Q4 = forms.CharField(label='Q4')
    Q5 = forms.CharField(label='Q5')
    Q6 = forms.CharField(label='Q6')
    Q7 = forms.CharField(label='Q7')
    Q8 = forms.CharField(label='Q8')
    Q9 = forms.CharField(label='Q9')
    Q10 = forms.CharField(label='Q10')
    Q11 = forms.CharField(label='Q11')
    Q12 = forms.CharField(label='Q12')
    Q13 = forms.CharField(label='Q13')
    Q14 = forms.CharField(label='Q14')
    Q15 = forms.CharField(label='Q15')
    Q16 = forms.CharField(label='Q16')
    Q17 = forms.CharField(label='Q17')
    Q18 = forms.CharField(label='Q18')
    Q19 = forms.CharField(label='Q19')
    Q20 = forms.CharField(label='Q20')
    Q21 = forms.CharField(label='Q21')
    Q22 = forms.CharField(label='Q22')
    Q23 = forms.CharField(label='Q23')
    Q24 = forms.CharField(label='Q24')
    Q25 = forms.CharField(label='Q25')
    Q26 = forms.CharField(label='Q26')
    Q27 = forms.CharField(label='Q27')
    Q28 = forms.CharField(label='Q28')
    Q29 = forms.CharField(label='Q29')
    Q30 = forms.CharField(label='Q30')
    Q31 = forms.CharField(label='Q31')
    Q32 = forms.CharField(label='Q32')
    Q33 = forms.CharField(label='Q33')
    Q34 = forms.CharField(label='Q34')
    Q35 = forms.CharField(label='Q35')
    Q36 = forms.CharField(label='Q36')
    Q37 = forms.CharField(label='Q37')
    Q38 = forms.CharField(label='Q38')
    Q39 = forms.CharField(label='Q39')
    Q40 = forms.CharField(label='Q40')
    Q41 = forms.CharField(label='Q41')
    Q42 = forms.CharField(label='Q42')
    Q43 = forms.CharField(label='Q43')
    Q44 = forms.CharField(label='Q44')
    Q45 = forms.CharField(label='Q45')
    Q46 = forms.CharField(label='Q46')
    Q47 = forms.CharField(label='Q47')
    Q48 = forms.CharField(label='Q48')
    Q49 = forms.CharField(label='Q49')
    Q50 = forms.CharField(label='Q50')
    Q51 = forms.CharField(label='Q51')
    Q52 = forms.CharField(label='Q52')
    Q53 = forms.CharField(label='Q53')
    Q54 = forms.CharField(label='Q54')
    Q55 = forms.CharField(label='Q55')
    Q56 = forms.CharField(label='Q56')
    Q57 = forms.CharField(label='Q57')
    Q58 = forms.CharField(label='Q58')
    Q59 = forms.CharField(label='Q59')
    Q60 = forms.CharField(label='Q60')
    Q61 = forms.CharField(label='Q61')
    Q62 = forms.CharField(label='Q62')
    Q63 = forms.CharField(label='Q63')
    Q64 = forms.CharField(label='Q64')
    Q65 = forms.CharField(label='Q65')
    Q66 = forms.CharField(label='Q66')
    Q67 = forms.CharField(label='Q67')
    Q68 = forms.CharField(label='Q68')
    Q69 = forms.CharField(label='Q69')
    Q70 = forms.CharField(label='Q70')
    Q71 = forms.CharField(label='Q71')
    Q72 = forms.CharField(label='Q72')
    Q73 = forms.CharField(label='Q73')
    Q74 = forms.CharField(label='Q74')
    Q75 = forms.CharField(label='Q75')
    Q76 = forms.CharField(label='Q76')
    Q77 = forms.CharField(label='Q77')
    Q78 = forms.CharField(label='Q78')
    Q79 = forms.CharField(label='Q79')
    Q80 = forms.CharField(label='Q80')
    Q81 = forms.CharField(label='Q81')
    Q82 = forms.CharField(label='Q82')
    Q83 = forms.CharField(label='Q83')
    Q84 = forms.CharField(label='Q84')
    Q85 = forms.CharField(label='Q85')
    Q86 = forms.CharField(label='Q86')
    Q87 = forms.CharField(label='Q87')
    Q88 = forms.CharField(label='Q88')
    Q89 = forms.CharField(label='Q89')
    Q90 = forms.CharField(label='Q90')
    Q91 = forms.CharField(label='Q91')
    Q92 = forms.CharField(label='Q92')
    Q93 = forms.CharField(label='Q93')
    Q94 = forms.CharField(label='Q94')
    Q95 = forms.CharField(label='Q95')
    Q96 = forms.CharField(label='Q96')
    Q97 = forms.CharField(label='Q97')
    Q98 = forms.CharField(label='Q98')
    Q99 = forms.CharField(label='Q99')
    Q100 = forms.CharField(label='Q100')
    Q101 = forms.CharField(label='Q101')
    Q102 = forms.CharField(label='Q102')
    Q103 = forms.CharField(label='Q103')
    Q104 = forms.CharField(label='Q104')
    Q105 = forms.CharField(label='Q105')
    Q106 = forms.CharField(label='Q106')
    Q107 = forms.CharField(label='Q107')
    Q108 = forms.CharField(label='Q108')
    Q109 = forms.CharField(label='Q109')
    Q110 = forms.CharField(label='Q110')
    Q111 = forms.CharField(label='Q111')
    Q112 = forms.CharField(label='Q112')
    Q113 = forms.CharField(label='Q113')
    Q114 = forms.CharField(label='Q114')
    Q115 = forms.CharField(label='Q115')
    Q116 = forms.CharField(label='Q116')
    Q117 = forms.CharField(label='Q117')
    Q118 = forms.CharField(label='Q118')
    Q119 = forms.CharField(label='Q119')
    Q120 = forms.CharField(label='Q120')
    Q121 = forms.CharField(label='Q121')
    Q122 = forms.CharField(label='Q122')
    Q123 = forms.CharField(label='Q123')
    Q124 = forms.CharField(label='Q124')
    Q125 = forms.CharField(label='Q125')
    Q126 = forms.CharField(label='Q126')
    Q127 = forms.CharField(label='Q127')
    Q128 = forms.CharField(label='Q128')
    Q129 = forms.CharField(label='Q129')
    Q130 = forms.CharField(label='Q130')
    Q131 = forms.CharField(label='Q131')
    Q132 = forms.CharField(label='Q132')
    Q133 = forms.CharField(label='Q133')
    Q134 = forms.CharField(label='Q134')
    Q135 = forms.CharField(label='Q135')
    Q136 = forms.CharField(label='Q136')
    Q137 = forms.CharField(label='Q137')
    Q138 = forms.CharField(label='Q138')
    Q139 = forms.CharField(label='Q139')
    Q140 = forms.CharField(label='Q140')
    Q141 = forms.CharField(label='Q141')
    Q142 = forms.CharField(label='Q142')
    Q143 = forms.CharField(label='Q143')
    Q144 = forms.CharField(label='Q144')
    Q145 = forms.CharField(label='Q145')
    Q146 = forms.CharField(label='Q146')
    Q147 = forms.CharField(label='Q147')
    Q148 = forms.CharField(label='Q148')
    Q149 = forms.CharField(label='Q149')
    Q150 = forms.CharField(label='Q150')
    Q151 = forms.CharField(label='Q151')
    Q152 = forms.CharField(label='Q152')
    Q153 = forms.CharField(label='Q153')
    Q154 = forms.CharField(label='Q154')
    Q155 = forms.CharField(label='Q155')
    Q156 = forms.CharField(label='Q156')
    Q157 = forms.CharField(label='Q157')
    Q158 = forms.CharField(label='Q158')
    Q159 = forms.CharField(label='Q159')
    Q160 = forms.CharField(label='Q160')
    Q161 = forms.CharField(label='Q161')
    Q162 = forms.CharField(label='Q162')
    Q163 = forms.CharField(label='Q163')
    Q164 = forms.CharField(label='Q164')
    Q165 = forms.CharField(label='Q165')
    Q166 = forms.CharField(label='Q166')
    Q167 = forms.CharField(label='Q167')
    Q168 = forms.CharField(label='Q168')
    Q169 = forms.CharField(label='Q169')
    Q170 = forms.CharField(label='Q170')
    Q171 = forms.CharField(label='Q171')
    Q172 = forms.CharField(label='Q172')
    Q173 = forms.CharField(label='Q173')
    Q174 = forms.CharField(label='Q174')
    Q175 = forms.CharField(label='Q175')
    Q176 = forms.CharField(label='Q176')
    Q177 = forms.CharField(label='Q177')
    Q178 = forms.CharField(label='Q178')
    Q179 = forms.CharField(label='Q179')
    Q180 = forms.CharField(label='Q180')
    Q181 = forms.CharField(label='Q181')
    Q182 = forms.CharField(label='Q182')
    Q183 = forms.CharField(label='Q183')
    Q184 = forms.CharField(label='Q184')
    Q185 = forms.CharField(label='Q185')
    Q186 = forms.CharField(label='Q186')
    Q187 = forms.CharField(label='Q187')
    Q188 = forms.CharField(label='Q188')
    Q189 = forms.CharField(label='Q189')
    Q190 = forms.CharField(label='Q190')
    Q191 = forms.CharField(label='Q191')
    Q192 = forms.CharField(label='Q192')
    Q193 = forms.CharField(label='Q193')
    Q194 = forms.CharField(label='Q194')
    Q195 = forms.CharField(label='Q195')
    Q196 = forms.CharField(label='Q196')
    Q197 = forms.CharField(label='Q197')
    Q198 = forms.CharField(label='Q198')
    Q199 = forms.CharField(label='Q199')
    Q200 = forms.CharField(label='Q200')
    class Meta:
        model = Question
        fields = "__all__"

#Formulaire de update d'un compte étudiant
class UpdateFormEtu(forms.Form):
    first_name = forms.CharField(label="first_name")
    last_name = forms.CharField(label="last_name")
    email = forms.EmailField(label="email")
    classeEtu = forms.ChoiceField(label="Class",choices=Classe_choices)
    promoEtu = forms.IntegerField(label="Prom")



class UpdateFormProf(forms.Form):
    first_name = forms.CharField(label="first_name")
    last_name = forms.CharField(label="last_name")
    email = forms.EmailField(label="email")

