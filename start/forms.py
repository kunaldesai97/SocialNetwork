
from django import forms
from django.contrib.auth.models import User
from . import models





class SignUpForm(forms.ModelForm):

    # male = 0
    # female = 1
    # CHOICES = ((male,'MALE'),(female,'FEMALE'))
    emailid = forms.EmailField()
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

class HomeForm(forms.Form):

    class Meta:
        model = models.Friends
  
  
class DateInput(forms.DateInput):
    input_type = 'date'
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['dob','profession','university','languages','hobbies','image']
        widgets = {
            'dob': DateInput(),
        }
        
class ImagePostForm(forms.ModelForm):
    
    class Meta:
        model = models.ImagePost
        fields = ['text','image']
        

# class UserHome(forms.ModelForm):





	   

    
		
