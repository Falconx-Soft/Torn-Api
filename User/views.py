from asyncio.proactor_events import constants
from turtle import right
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
import pandas as pd
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

def addData(request):
	chk = pd.read_excel("data.xlsx")
	data = chk.values.tolist()
	for d in data:
		temp = d[0].split(" ")
		if len(temp) != 1:
			db_user_id = temp[1].strip("[]")
		else:
			db_user_id = temp[0].strip("[]")
		db_faction = d[2]
		db_totalStats = d[8]
		db_str = d[4]
		db_def = d[5]
		db_spd = d[6]
		db_dex = d[5]
		record_obj = record(UserId=db_user_id,Faction=db_faction,TotalStats=db_totalStats,Str=db_str,Def=db_def,Spd=db_spd,Dex=db_dex)
		record_obj.save()

def apiView(request):
	user_info = apiInfo.objects.get(user=request.user)
	key = user_info.apiKey
	record_obj = record.objects.all()

	page = request.GET.get('page')
	results = 5
	paginator = Paginator(record_obj,results)

	try:
		record_obj = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		record_obj = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
		record_obj = paginator.page(page)

	leftIndex = (int(page) - 1)

	if leftIndex < 1:
		leftIndex = 1

	rightIndex = (int(page) + 5)

	if rightIndex > paginator.num_pages:
		rightIndex = paginator.num_pages + 1

	custom_range = range(leftIndex, rightIndex)

	data_list = []
	faction_list = []


	x = 0
	for r in record_obj:
		x = x+1
		try:
			print(x,r.UserId)
			data = requests.get('https://api.torn.com/user/'+r.UserId+'?selections=&key='+key+'')
			json_data = data.json()
			name = json_data["name"]
			status = json_data["status"]["description"]
			level = json_data["level"]
			age = json_data["age"]
			lastAction = json_data["last_action"]["relative"]
			data_info = {
				'name':name,
				'status':status,
				'level':level,
				'age':age,
				'lastAction':lastAction,
				'faction':r.Faction,
				'total_stats':r.TotalStats,
				'str':r.Str,
				'def':r.Def,
				'spd':r.Spd,
				'dex':r.Dex,
				'user_id':r.UserId,
			}
			data_list.append(data_info)
			if r.Faction not in faction_list:
				faction_list.append(r.Faction)
		except:
			print("Error at...",x,r.UserId)
	context = {
		'data_list':data_list,
		'faction_list':faction_list,
		'paginator':paginator,
		'record_obj':record_obj,
		'custom_range':custom_range,
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