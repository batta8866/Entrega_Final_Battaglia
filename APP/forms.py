from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from APP.models import *


class formulario_registro (UserCreationForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Ingrese la Contraseña" , widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repita la Contraseña" , widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username" , "first_name" , "last_name" , "email" , "password1" , "password2"]



#class PostForm (forms.ModelForm):
#    class Meta:
#        model = posteo
#        fields = "__all__"
#      # exclude = ("autor" ,)
#        widgets = {"titulo": forms.TextInput(attrs={"class":"form-control" , "placeholder":"Titulo"}) ,
#                    "autor": forms.TextInput(attrs={"class":"form-control" , "value":"" , "id":"TTLLOO" , "type":"hidden"}) ,
#                    
#                    #"autor": forms.Textarea(attrs={"class":"form-control" , "placeholder": (models.ForeignKey(User , on_delete=models.CASCADE))}) ,
#                    "body": forms.Textarea (attrs={"class":"form-control"})}
                    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name" , "last_name" , "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


class PostForm (forms.ModelForm):
    class Meta:
        model = posteo
        fields = ["titulo" , "body"]


class AddComentForm (forms.ModelForm):
    class Meta:
        model = Coment
        fields = ["body"]
        widgets = {"body": forms.Textarea (attrs={"class":"form-control"})}
