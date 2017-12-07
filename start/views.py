from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, HomeForm, ProfileForm, ImagePostForm
from .models import Person, Friends
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import messages 
from django.core.urlresolvers import reverse
from django.db import connection, connections
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from OpenSSL.rand import load_file
# Create your views here.

cursor = connection.cursor()
# SignUp Page	
class UserFormView(View):
	form_class = SignUpForm
	template_name = 'start/signup_form.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	def post(self,request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			name = form.cleaned_data['name']
			emailid = form.cleaned_data['emailid']					
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			gender = form.cleaned_data['gender']

			user.set_password(password)
			user.insert()
			request.session['name'] = username
			return HttpResponseRedirect('/user/%s' %username)


		return render(request, self.template_name,{'form':form})

#Login Page
class LoginFormView(View):
	form_class = LoginForm
	template_name  = 'start/home.html'
	def get(self, request):
		form = self.form_class(None)
		cache.clear()
		return render(request, self.template_name, {'form':form})


	def post(self, request):
		form = self.form_class(request.POST)
		username =request.POST['username']
		password =request.POST['password']
		cursor.execute('SELECT username FROM Person')

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
        
		cursor.execute('SELECT password FROM Person WHERE username = %s',[username])
		user = cursor.fetchone()
	


		if(user[0] == password):
			request.session['name'] = username
			return HttpResponseRedirect('user/%s' %username)
		else:
			wrongpassword = True
			form = self.form_class(None)
			context = {'wrongpassword': wrongpassword, 'form': form}
			return render(request, 'start/home.html', context)

		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})


#Returns friends'username and their name
def friendname(user):
	cursor.execute('SELECT recipient_id FROM Friends WHERE sender_id = %s AND accepted = 1',[user[0][0]])
	result1 = list(cursor.fetchall())
	cursor.execute('SELECT sender_id FROM Friends WHERE recipient_id = %s AND accepted = 1',[user[0][0]])
	result2 = cursor.fetchall()
	for i in result2:
		result1.append(i[0])
	friendid = []
	for i in result1:
		friendid.append(i)
		
	friendusername = []
	for i in friendid:
		cursor.execute('SELECT username FROM Person WHERE user_id = %s',[i])
		result = cursor.fetchone()
		friendusername.append(result[0])
	friend_name = []
	for i in friendid:
		cursor.execute('SELECT name FROM Person WHERE user_id = %s',[i])
		result = cursor.fetchone()
		friend_name.append(result[0])
	return list(zip(friendusername,friend_name))

#Returns the friend request sender's name
def friendreq(user):
	friendreq_id = friendreqid(user)
	friendreq_name = []
	for i in friendreq_id:
		cursor.execute('SELECT name FROM Person WHERE user_id = %s',[i])
		result = cursor.fetchone()
		friendreq_name.append(result[0])
	return friendreq_name


#Returns the friend request sender's username
def friendrequsername(user):
	friendreq_id = friendreqid(user)
	friendreq_username = []
	for i in friendreq_id:
		cursor.execute('SELECT username FROM Person WHERE user_id = %s',[i])
		result = cursor.fetchone()
		friendreq_username.append(result[0])
	return friendreq_username


#Returns the friend request sender's user_id
def friendreqid(user):
	friendreq_id = []
	cursor.execute('SELECT sender_id FROM Friends WHERE recipient_id = %s AND rejected = 0 AND accepted = 0',[user[0][0]])
	result = cursor.fetchall()
	for i in result:
		friendreq_id.append(i[0])
	return friendreq_id

#Returns the user_id of person whose friend request is rejected
def friendreject(user):
	friend_reject = []
	cursor.execute('SELECT sender_id FROM Friends WHERE recipient_id = %s AND rejected = 1',[user[0][0]])
	result = cursor.fetchone()
	if result!= None:
		for i in result:
			friend_reject.append(i)
	return friend_reject


#Returns details of other users in network
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
			
	people_username = []
	for i in people_id:
		cursor.execute('SELECT username FROM Person WHERE user_id = %s',[i])
		res = cursor.fetchone()
		people_username.append(res[0])
	people_name=[]
	for i in people_id:
		cursor.execute('SELECT name FROM Person WHERE user_id = %s',[i])
		res = cursor.fetchone()
		people_name.append(res[0])
	people = list(zip(people_id,people_name,people_username))
	return people


#To accept the friend request
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
		
		
#To reject the friend request
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
	
#To send request to other users
def sendreq(request,reqid,seid):
	cursor.execute('INSERT INTO Friends VALUES(%s,%s,%s,%s)',[seid,reqid,0,0])
	return HttpResponse('Request Sent')


#News Feed Page
def homepage(request,username):
	if 'name' in request.session.keys():
		if request.session['name']==username:
			cursor.execute('SELECT * FROM Person WHERE username = %s',[username])
			user = cursor.fetchall()
			friend_id = friendid(user)
			friend_id.append(user[0][0])
			cursor.execute('SELECT * FROM image_post ORDER BY time DESC')
			res = cursor.fetchall()
			name = []
			text = []
			image = []
			imageid = []
			likes = []
			for i in res:
				if i[0] in friend_id:
					cursor.callproc('friend_name', [i[0]])
					res1 = cursor.fetchall()
					name.append(res1[0][0])
					text.append(i[1])
					image.append(i[2])
					imageid.append(i[4])
					likes.append(i[5])
			userlike = []
			for i in imageid:
				cursor.execute('SELECT user_id FROM likes WHERE image_id = %s',[i])
				res1 = [res[0] for res in cursor.fetchall()]
				
				if(len(res1)==0):
					userlike.append(0)
				else:
					if(user[0][0] in res1):
						userlike.append(1)
					else:
						userlike.append(0)
			
			post = list(zip(name,text,image,imageid,likes,userlike))
			context = {'user_id':user[0][0],'name':user[0][1],'username':username,'post':post}
			return render(request,'user/homepage.html',context)
		else:
			return HttpResponse('You are logged out')
	
	else:
		return HttpResponse('You are logged out')

#Returns the list of friends, friend requests and people the user may know
def friends(request,username):
	if 'name' in request.session.keys():
		if request.session['name']==username:
			cursor.execute('SELECT * FROM Person WHERE username = %s',[username])
			user = cursor.fetchall()
			friend = friendname(user)
			friendreq_name = friendreq(user)
			friendreq_username = friendrequsername(user)
			friendreq_id = friendreqid(user)
			friendrequest 	= list(zip(friendreq_name,friendreq_id,friendreq_username))
			people = mayknow(user)
			context = {'name':user[0][1],'id':user[0][0],'username':username,'friend':friend,'request':friendrequest,'mayknow':people}
			return render(request,'user/friends.html',context)
		else:
			return HttpResponse('You are logged out')
	
	else:
		return HttpResponse('You are logged out')
			

#To create a profile for user
class ProfileFormView(View):
	form_class = ProfileForm
	template_name = 'user/profile.html'

	def get(self, request, username):
		if 'name' in request.session.keys():
			if request.session['name']==username:
				form = self.form_class(None)
				cursor.execute('SELECT user_id FROM Person WHERE username = %s',[username])
				res = cursor.fetchall()
				cursor.execute('SELECT user_id FROM Profile WHERE user_id = %s',[res[0][0]])
				res = cursor.fetchall()
				if(len(res) == 0):	
					cursor.execute('SELECT * FROM Person WHERE username = %s',[username])
					user = cursor.fetchall()
					context = {'name':user[0][1],'username':username,'form':form}
					return render(request, self.template_name,context)
				else:
					return HttpResponseRedirect('/user/displayprofile/%s' %username)
			else:
				return HttpResponse('You are logged out')
		else:
			return HttpResponse('You are logged out')
	def post(self, request,username):
		form = self.form_class(request.POST,request.FILES)

		if form.is_valid():
			user = form.save(commit=False)                
			dob = form.cleaned_data['dob']
			profession = form.cleaned_data['profession']	
			university = form.cleaned_data['university']
			languages = form.cleaned_data['languages']
			hobbies = form.cleaned_data['hobbies']
			cursor.execute('SELECT user_id, name, emailid, gender from Person WHERE username = %s',[username])
			res = cursor.fetchall()
			user_id = res[0][0]
			name = res[0][1]
			email_id = res[0][2]
			gender = res[0][3]
			if 'image' not in request.FILES.keys():
				image = '/media/default.png';
				cursor.execute('INSERT INTO Profile VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[user_id,name,email_id,dob,profession,university,languages,hobbies,image,gender])
			else:
				image = request.FILES['image']
				user.user_id = user_id;
				user.name = name;
				user.email_id = email_id
				user.gender = gender
				user.save() 
				cursor.execute('UPDATE Profile set gender =%s where user_id = %s',[gender,user_id])
				return HttpResponseRedirect('/user/displayprofile/%s' %username)
            
		cursor.execute('SELECT * FROM Person WHERE username = %s',[username])
		user = cursor.fetchall()
		context = {'name':user[0][1],'username':username,'form':form}
		return render(request, self.template_name,context)


#Display user's profile
def displayProfile(request,username):
	cursor.execute('SELECT * FROM Person WHERE username = %s',[username])
	user = cursor.fetchall()
	email = user[0][5]
	
	cursor.execute('SELECT * FROM Profile WHERE email_id = %s',[email])
	prof = cursor.fetchall()
	
	if(len(prof)==0):
		cursor.execute('SELECT name, gender FROM Person WHERE username = %s',[username])
		res = cursor.fetchall()
		pic = 'media/default.png'
		if(res[0][1]=='F'):
			gender = 'Female'
		else:
			gender = 'Male'
		context = {'name':res[0][0],'email':email,'gender':gender,'pic':pic}
		return render(request,'user/nodisplay.html',context)
	else:
		cursor.execute('SELECT image from Profile WHERE email_id = %s',[email])
		image  = cursor.fetchall()
		pic = image[0][0]
		if(prof[0][9]=='F'):
			gender = 'Female'
		else:
			gender = 'Male'
		context = {'name':prof[0][1],'email':prof[0][2],'dob':prof[0][3],'profession':prof[0][4],
			'university':prof[0][5],'languages':prof[0][6],'hobbies':prof[0][7],'gender':gender,"pic":pic}
		return render(request,'user/display.html',context)
	
	
#To post image on News Feed
class ImagePostFormView(View):
	form = form_class = ImagePostForm
	template_name = 'user/imagepost.html'
	
	def get(self, request, username):
		if 'name' in request.session.keys():
			if request.session['name']==username:
				form = self.form_class(None)
				return render(request,self.template_name,{'form':form})
			else:
				return HttpResponse('You are logged out')
			
		else:
			return HttpResponse('You are logged out')
		
	def post(self, request, username):
		form = self.form_class(request.POST,request.FILES)
		if form.is_valid():
			cursor.execute('SELECT user_id FROM Person WHERE username = %s',[username])
			res = cursor.fetchall()
			user_id = res[0][0]
			user = form.save(commit=False)
			text = form.cleaned_data['text']
			image = request.FILES['image']
			user.user_id = user_id
			user.text = text;
			user.save()
			return HttpResponseRedirect('/user/%s' %username)
	
#Returns the user_id of friends
def friendid(user):
	cursor.execute('SELECT recipient_id FROM Friends WHERE sender_id = %s AND accepted = 1',[user[0][0]])
	result1 = [res[0] for res in cursor.fetchall()]
	cursor.execute('SELECT sender_id FROM Friends WHERE recipient_id = %s AND accepted = 1',[user[0][0]])
	result2 = [res[0] for res in cursor.fetchall()]
	for i in result2:
		result1.append(i)
	friend_id = []
	for i in result1:
		friend_id.append(i)
	return friend_id

#To insert the user_id of user who has liked the image post.
def like(request,image_id,user_id):
	cursor.execute('INSERT INTO likes VALUES(%s,%s)',[user_id,image_id])
	

#To logout from the account
def logout(request):
		del request.session['name']
		request.session.flush()
		return HttpResponseRedirect('/')
     
     