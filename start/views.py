from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, HomeForm
from .models import Person, Friends
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import messages 
from django.core.urlresolvers import reverse
from django.db import connection, connections
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
# Create your views here.

cursor = connection.cursor()

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
		cache.clear()
		return render(request, self.template_name, {'form':form})


	def post(self, request):
		form = self.form_class(request.POST)
    		# user = form.save(commit=False)
    		# return HttpResponse('Successfully logged in')
		username =request.POST['username']
		password =request.POST['password']
		cursor.execute('SELECT username FROM Person')

		# if(username not in Person.objects.all().values_list('username', flat = True)):
		# 	invaliduser = True
		# 	form = self.form_class(None)
		# 	context = {'invaliduser': invaliduser, 'form': form}
		# 	return render(request, 'start/home.html', context)
		user = cursor.fetchall()
		found = False
		for i in user:
			if username == i[0]:
				found = True
		if(found == False):
			invaliduser = True
			form = self.form_class(None)
			context = {'invaliduser': invaliduser, 'form': form}
			return render(request, 'start/home.html', context)
        
		# user =  Person.objects.get(username=username)
		# if(user==None):
		# 	invaliduser = True
		# 	form = self.form_class(None)
		# 	context = {'invaliduser': invaliduser, 'form': form}
		# 	return render(request, 'start/home.html', context)
		cursor.execute('SELECT password FROM Person WHERE username = %s',[username])
		user = cursor.fetchone()
	


		if(user[0] == password):
			# return HttpResponse('Successfully logged in as'+' '+ user.name)
			# return HttpResponseRedirect('user/%s',%username)
			return HttpResponseRedirect('user/%s' %username)
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


def accept(request):
	return HttpResponse('Friend Request Accepted')
	

def userhome(request,username):
	cursor.execute('SELECT * FROM Person WHERE username = %s',[username])
	user = cursor.fetchall()
	friend_name = friendname(user)
	friendreq_name = friendreq(user)
	friendreq_id = friendreqid(user)
	friend_reject = friendreject(user)
	friendrequest = list(zip(friendreq_name,friendreq_id))
	print(friendrequest)
	people = mayknow(user)
# 	print(friendrequest)
	context = {'name':user[0][1],'id':user[0][0],'friend':friend_name,'request':friendrequest,'reject':friend_reject,'mayknow':people}
	return render(request,'user/home.html',context)

def friendname(user):
	cursor.execute('SELECT recipient_id FROM Friends WHERE sender_id = %s AND accepted = 1',[user[0][0]])
	result1 = list(cursor.fetchall())
# 	print(result1)
	cursor.execute('SELECT sender_id FROM Friends WHERE recipient_id = %s AND accepted = 1',[user[0][0]])
	result2 = cursor.fetchall()
	for i in result2:
		result1.append(i[0])
	friendid = []
	for i in result1:
		friendid.append(i)
	friend_name = []
	for i in friendid:
		cursor.execute('SELECT name FROM Person WHERE user_id = %s',[i])
		result = cursor.fetchone()
		friend_name.append(result[0])
	return friend_name

def friendreq(user):
	friendreq_id = friendreqid(user)
	friendreq_name = []
	for i in friendreq_id:
		cursor.execute('SELECT name FROM Person WHERE user_id = %s',[i])
		result = cursor.fetchone()
		friendreq_name.append(result[0])
	return friendreq_name

def friendreqid(user):
	friendreq_id = []
	cursor.execute('SELECT sender_id FROM Friends WHERE recipient_id = %s AND rejected = 0 AND accepted = 0',[user[0][0]])
	result = cursor.fetchall()
	print(result)
	for i in result:
		friendreq_id.append(i[0])
	return friendreq_id

def friendreject(user):
	friend_reject = []
	cursor.execute('SELECT sender_id FROM Friends WHERE recipient_id = %s AND rejected = 1',[user[0][0]])
	result = cursor.fetchone()
	if result!= None:
		for i in result:
			friend_reject.append(i)
	return friend_reject

def mayknow(user):
	people_id = []
	cursor.execute('SELECT user_id FROM Person WHERE user_id <> %s',[user[0][0]])
	res = cursor.fetchall()
	senders = []
	recipients = []
	cursor.execute('SELECT sender_id FROM Friends WHERE recipient_id = %s',[user[0][0]])
	senders = cursor.fetchall()
	cursor.execute('SELECT recipient_id FROM Friends WHERE sender_id = %s',[user[0][0]])
	recipients = cursor.fetchall()
# 	print(senders)
# 	print(recipients)
	for i in res:
		flag = True
		for j in senders:
			if i[0] == j[0]:
				flag = False
		
		for j in recipients:
			if i[0] == j[0]:
				flag = False
		if flag == True:
			people_id.append(i[0])
	people_name=[]
	for i in people_id:
		cursor.execute('SELECT name FROM Person WHERE user_id = %s',[i])
		res = cursor.fetchone()
		people_name.append(res[0])
	people = list(zip(people_id,people_name))
	return people

class AcceptView(View):
	form_class = HomeForm
	template_name = 'user/home.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	def post(self,request,seid,reid):
		form = self.form_class(request.POST)
		print(id)
		cursor = connection.cursor()
		cursor.execute('UPDATE friends SET accepted = %s WHERE sender_id = %s AND recipient_id = %s',[1,int(seid),int(reid)])
		return HttpResponse("Friend Request Accepted")
		
class RejectView(View):
	form_class = HomeForm
	template_name = 'user/home.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	def post(self,request,seid,reid):
		form = self.form_class(request.POST)
		cursor = connection.cursor()
		cursor.execute('UPDATE friends SET accepted = %s WHERE sender_id = %s AND recipient_id = %s',[0,int(seid),int(reid)])
		cursor.execute('UPDATE friends SET rejected = %s WHERE sender_id = %s AND recipient_id = %s',[1,int(seid),int(reid)])
		return HttpResponse("Friend Request ")
	
	
def sendreq(request,reqid,seid):
	print(reqid)
	cursor.execute('INSERT INTO Friends VALUES(%s,%s,%s,%s)',[seid,reqid,0,0])
	return HttpResponse('Request Sent')


def homepage(request,username):
	cursor.execute('SELECT * FROM Person WHERE username = %s',[username])
	user = cursor.fetchall()
	print(user[0][1])
	context = {'name':user[0][1],'username':username}
	return render(request,'user/homepage.html',context)

def friends(request,username):
	cursor.execute('SELECT * FROM Person WHERE username = %s',[username])
	user = cursor.fetchall()
	friend_name = friendname(user)
	friendreq_name = friendreq(user)
	friendreq_id = friendreqid(user)
	friendrequest = list(zip(friendreq_name,friendreq_id))
	people = mayknow(user)
	context = {'name':user[0][1],'id':user[0][0],'username':username,'friend':friend_name,'request':friendrequest,'mayknow':people}
	return render(request,'user/friends.html',context)
	