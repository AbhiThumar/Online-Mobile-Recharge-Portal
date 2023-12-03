import re
from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserProfileForm
from .models import Profile,transactions
import requests
from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse,JsonResponse 

from django.contrib import auth 
import pyrebase
from django.contrib.sessions.middleware import SessionMiddleware
import io
from PIL import Image

import firebase_admin
from firebase_admin import db

from django.core.files.base import File
from django.db import models
# Create your views here.

#Jay 

config={
	"apiKey": "AIzaSyBOSZKBZQYdcHmaCs5nlOhrD9GGVuiVRFU",
    "authDomain": "mobile-recharge-a2f5b.firebaseapp.com",
    "projectId": "mobile-recharge-a2f5b",
    "storageBucket": "mobile-recharge-a2f5b.appspot.com",
    "messagingSenderId": "220946121042",
    "appId": "1:220946121042:web:402e08cd8a20f377ecba8b",
    "measurementId": "G-6JZEK2YC24",
    "serviceAccount" : "D:/Academics/DA-IICT/Semester-5/Software Engineering/project/Online-Mobile-Recharge-Portal/Project/backend/otp-authentication-with-django/serviceAccount.json",
    "databaseURL" : "https://mobile-recharge-a2f5b-default-rtdb.firebaseio.com/",
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage = firebase.storage()

storage = firebase.storage()

Ans = database.child("Admin").child("Operators").get()
key=[]
for det in Ans.each():
    key.append(det.key())
print(key)

         
def recharge_now(request):
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
            print(det.key())
            key.append(det.key())
    context = {
        "list_data": key,
    }
    return render(request , 'Recharge_Now.html',context)


def plans(request):
    Mobile_Operator = request.POST.get('Mobile_Operator')
    Select_Plans = request.POST.get('Select_Plans')

    Ans = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).get()
    key=[]
    for det in Ans.each():
            key.append(det.key())

    list_data_dict=[]

    for id in key:
        Amount = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Amount").get()
        Validity = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Validity").get()
        SMS = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("SMS").get()
        Talktime = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Talktime").get()
        Full_Talktime = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Full_Talktime").get()
        Data = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Data").get()
        Value_Added_Services = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Value_Added_Services").get()
        
        list_data_dict.append([Mobile_Operator , Select_Plans , id , Amount.val() , Validity.val(),
                                SMS.val() , Talktime.val() ,Full_Talktime.val() ,Data.val() , Value_Added_Services.val()])

    context = {
        "list_data": list_data_dict,
    }
    return render(request , 'View_Plans.html' , context)


def offers(request):
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    context = {
        "list_data": key,
    }
    return render(request , 'View_Offers.html' , context)

def offs(request):
    Mobile_Operator = request.POST.get('Mobile_Operator')

    Ans = database.child("Admin").child("Operators").child(Mobile_Operator).child("Offers").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())


    list_data_dict=[]

    for id in key:
        Name = database.child("Admin").child("Operators").child(Mobile_Operator).child("Offers").child(id).child("Mobile_Operator").get()
        Offer_Type = database.child("Admin").child("Operators").child(Mobile_Operator).child("Offers").child(id).child("Offer_Type").get()
        Validity = database.child("Admin").child("Operators").child(Mobile_Operator).child("Offers").child(id).child("Validity").get()
        Des = database.child("Admin").child("Operators").child(Mobile_Operator).child("Offers").child(id).child("Description").get()
        list_data_dict.append([Name.val() , id , Offer_Type.val() , Validity.val() , Des.val()])


    context = {
        "list_data": list_data_dict,
    }
    return render(request , 'View_Offs.html',context)


#Charith

def send_otp(number,message):
    url = "https://www.fast2sms.com/dev/bulk"
    api = "ia3ozpZDS3xrTfpzc3sCWbg9vPZmeH15Qur9y3l6sxVzoOrL77T6ZGJXiFDz"
    querystring = {"authorization":api,"sender_id":"FSTSMS","message":message,"language":"english","route":"p","numbers":number}
    headers = {
        'cache-control': "no-cache"
    }
    return requests.request("GET", url, headers=headers, params=querystring)

    
def Registration(request):
    if request.method == "POST":
        fm = UserRegistrationForm(request.POST)
        up = UserProfileForm(request.POST)
        if fm.is_valid() and up.is_valid():
            e = fm.cleaned_data['email']
            u = fm.cleaned_data['username']
            p = fm.cleaned_data['password1']
            request.session['email'] = e
            request.session['username'] = u
            request.session['password'] = p
            p_number = up.cleaned_data['phone_number']
            request.session['number'] = p_number

            UserName = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            mobile = request.POST.get('phone_number')
            Gender = request.POST.get('gender')
            Mobile_Operator= request.POST.get('Mobile_Operator')
            Date_Of_Birth = request.POST.get('Date_Of_Birth')
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            message = f'your otp is {otp}'
            send_otp(p_number,message)
            

            data={"UserName" : UserName ,"Mobile_Number" : mobile,
                    "Email" : email , "Password":password,"Gender" : Gender ,
                    "Mobile_Operator" : Mobile_Operator,"Date_Of_Birth" : Date_Of_Birth }

            database.child("Users").child(mobile+ '_' + UserName).child("Details").set(data)
            Ans = database.child("Admin").child("Operators").get()
            key=[]
            for det in Ans.each():
                    key.append(det.key())
            context = {
                "list_data": key,
            }
            return render(request, 'registration.html', context)
    else:
        fm  = UserRegistrationForm()
        up = UserProfileForm()
    context = {'fm':fm,'up':up}
    return render(request,'registration.html',context)


def otpRegistration(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session.get('otp')
        user = request.session['username']
        hash_pwd = make_password(request.session.get('password'))
        p_number = request.session.get('number')
        email_address = request.session.get('email') 

        if int(u_otp) == otp:
            User.objects.create(
                            username = user,
                            email=email_address,
                            password=hash_pwd
            )
            user_instance = User.objects.get(username=user)
            Profile.objects.create(
                            user = user_instance,phone_number=p_number
            )
            request.session.delete('otp')
            request.session.delete('user')
            request.session.delete('email')
            request.session.delete('password')
            request.session.delete('phone_number')

            messages.success(request,'Registration Successfully Done !!')

            return redirect('/login/')
        
        else:
            messages.error(request,'Wrong OTP')


    return render(request,'registration-otp.html')


def userLogin(request):

    try :
        if request.session.get('failed') > 2:
            return HttpResponse('<h1> You have to wait for 5 minutes to login again</h1>')
    except:
        request.session['failed'] = 0
        request.session.set_expiry(100)



    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            request.session['username'] = username
            request.session['password'] = password
            u = User.objects.get(username=username)
            p = Profile.objects.get(user=u)
            p_number = p.phone_number
            otp = random.randint(1000,9999)
            request.session['login_otp'] = otp
            message = f'your otp is {otp}'
            send_otp(p_number,message)
            return redirect('/login/otp/')
        else:
            messages.error(request,'username or password is wrong')
    return render(request,'login.html')

def otpLogin(request):
    if request.method == "POST":
        username = request.session['username']
        password = request.session['password']
        otp = request.session.get('login_otp')
        u_otp = request.POST['otp']
        if int(u_otp) == otp:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                request.session.delete('login_otp')
                messages.success(request,'login successfully')
                return redirect('Recharge_Now')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'login-otp.html')

def home(request):
    if request.method == "POST":
        otp = random.randint(1000,9999)
        request.session['email_otp'] = otp
        message = f'your otp is {otp}'
        user_email = request.user.email

        send_mail(
            'Email Verification OTP',
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
        return redirect('/email-verify/')

    return render(request,'home.html')

def mytrans(request):
    t = transactions.objects.filter(sender = request.user.username).order_by('-id')|transactions.objects.filter(receiver = request.user.username).order_by('-id')
    return render(request,'transaction.html',{'mytr':t})

