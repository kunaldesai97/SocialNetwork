
from django import forms
from django.contrib.auth.models import User
from . import models
class SignUpForm(forms.ModelForm):

    # male = 0
    # female = 1
    # CHOICES = ((male,'MALE'),(female,'FEMALE'))
    password = forms.CharField(widget=forms.PasswordInput)
    # gender = forms.ChoiceField(choices = CHOICES, widget=forms.RadioSelect())
    # username = forms.CharField(unique = True)
    
    class Meta:
	    model = models.Person
	    fields = ['name','emailid','username','password','gender']


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.Person
        fields = ['username','password']



	   

    
		
