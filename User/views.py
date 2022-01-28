from asyncio.proactor_events import constants
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CutomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import*
import uuid
from django.conf import settings
from django.core.mail import send_mail
import requests

# Create your views here.
@login_required(login_url='login')
def home(request):
	
	if request.method == 'POST':
		apiKey = request.POST['apiKey']
		user = request.user
		info = apiInfo(apiKey=apiKey,user=user)
		info.save()
	try:
		apiInfo.objects.get(user=request.user)
		return redirect('apiView')
	except:
		pass
	return render(request,'User/home.html')

def apiView(request):
	user_info = apiInfo.objects.get(user=request.user)
	key = user_info.apiKey
	record_obj = record.objects.all()
	data_list = []
	faction_list = []
	for r in record_obj:
		data = requests.get('https://api.torn.com/user/'+r.UserId+'?selections=&key='+key+'')
		json_data = data.json()
		name = json_data["name"]
		status = json_data["status"]["description"]
		level = json_data["level"]
		age = json_data["age"]
		lastAction = json_data["last_action"]["relative"]
		faction = json_data["faction"]["faction_name"]
		if faction not in faction_list:
			faction_list.append(faction)
		data_info = {
			'name':name,
			'status':status,
			'level':level,
			'age':age,
			'lastAction':lastAction,
			'faction':faction,
			'total_stats':r.TotalStats,
			'str':r.Str,
			'def':r.Def,
			'spd':r.Spd,
			'dex':r.Dex
		}
		data_list.append(data_info)
	context = {
		'data_list':data_list,
		'faction_list':faction_list
	}
	return render(request,'User/apiView.html',context)

def loginUser(request):

	if request.user.is_authenticated:
		return redirect('home')
	msg = None
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			user = User.objects.get(username=username)
			user = authenticate(request, username=username, password=password) # check password

			if user is not None and accountsCheck.objects.get(user=user).is_verified:
				login(request, user)
				return redirect('home')
			else:
				msg = 'User/Something is wrong'
		except:
			msg = 'User not recognized.'
	context = {
		'msg':msg
	}
	return render(request,'User/login.html',context)

def register(request):
	msg = None
	form = CutomUserCreationForm
	if request.method == 'POST':
		form = CutomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			# user.username = user.username.lower()
			user.save()

			auth_token = str(uuid.uuid4())
			accountsCheck_obj = accountsCheck.objects.create(user=user, auth_token = auth_token)
			accountsCheck_obj.save()

			verificationMain(user.email,auth_token)

			return redirect('login')
		else:
			msg = 'Error.'
	context = {'form':form, 'msg':msg}
	return render(request,'User/register.html', context)

def verify(request, auth_token):
	accountsCheck_obj = accountsCheck.objects.get(auth_token = auth_token)
	if accountsCheck:
		accountsCheck_obj.is_verified = True
		accountsCheck_obj.save()
		return redirect('login')

def verificationMain(email, auth_token):
	subject = 'Please verify your account'
	message = f'Hi please click on the link to verify your account http://localhost:8000/verify/{auth_token}'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [email]
	send_mail(subject,message,email_from, recipient_list)

def logoutUser(request):
	logout(request)
	return redirect('login')