
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm
from .models import Person
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import messages 

# Create your views here.

def index(request):
	return render(request, 'start/home.html')
	
class UserFormView(View):
	form_class = SignUpForm
	template_name = 'start/signup_form.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	def post(self,request):
		form = self.form_class(request.POST)

		if form.is_valid():
			# return HttpResponse('Successfully signed in')
			user = form.save(commit=False)
			name = form.cleaned_data['name']
			emailid = form.cleaned_data['emailid']					
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			gender = form.cleaned_data['gender']

			user.set_password(password)
			user.insert()
			return HttpResponse('Successfully signed in')
			# list = []
			# if(username not in people.objects.all().values_list('username', flat=True)):
			#     user.save()
			# else:
			# 	form.inuser()


			# user = authenticate(username = username, password = password)

			# if user is not None:

			# 	if user.is_active:
			# 		login(request, user)
			# 		return redirect('../')
			# 		# return HttpResponse('Successfully signed in')


		return render(request, self.template_name,{'form':form})


class LoginFormView(View):
	form_class = LoginForm
	template_name  = 'start/home.html'
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})


	def post(self, request):
		form = self.form_class(request.POST)
    		# user = form.save(commit=False)
    		# return HttpResponse('Successfully logged in')
		username =request.POST['username']
		password =request.POST['password']

		if(username not in Person.objects.all().values_list('username', flat = True)):
			invaliduser = True
			form = self.form_class(None)
			context = {'invaliduser': invaliduser, 'form': form}
			return render(request, 'start/home.html', context)
        
		user =  Person.objects.get(username=username)
		# if(user==None):
		# 	invaliduser = True
		# 	form = self.form_class(None)
		# 	context = {'invaliduser': invaliduser, 'form': form}
		# 	return render(request, 'start/home.html', context)
 
		print(user.password)


		if(user.password == password):
			return HttpResponse('Successfully logged in as'+' '+ user.name)
		else:
			wrongpassword = True
			form = self.form_class(None)
			context = {'wrongpassword': wrongpassword, 'form': form}
			return render(request, 'start/home.html', context)

		# user.set_password(password)
		# print(username)
		# print(password)
		# list = people.objects.all().values_list('username','password')
		# print(list)
		# if(username,password in list):
		# 	return HttpResponse('Successfully logged in')
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	# def post(self,request):
	# 	form = self.form_class(request.POST)

	# 	user = form.save(commit=False)
	# 	username = form.cleaned_data['username']
	# 	password = form.cleaned_data['password']

	# 	user.set_password(password)

	# 	list = people.objects.all().values_list('username','password')

	# 	if(username,password in list):
	# 		return HttpResponse('Successfully logged in')


	# 	return render(request, self.template_name,{'form':form})
		











