from django.shortcuts import render
from django.contrib import auth,messages 
import pyrebase
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from django.http import HttpResponse, JsonResponse 

import pytz
import io
from PIL import Image
from datetime import datetime

import firebase_admin
from firebase_admin import db

from django.core.files.base import File
from django.db import models
from django.utils import timezone





config={
	"apiKey": "AIzaSyBOSZKBZQYdcHmaCs5nlOhrD9GGVuiVRFU",
    "authDomain": "mobile-recharge-a2f5b.firebaseapp.com",
    "projectId": "mobile-recharge-a2f5b",
    "storageBucket": "mobile-recharge-a2f5b.appspot.com",
    "messagingSenderId": "220946121042",
    "appId": "1:220946121042:web:402e08cd8a20f377ecba8b",
    "measurementId": "G-6JZEK2YC24",
    "serviceAccount" : "E:/Django/Try1/try/try/serviceAccount.json",
    "databaseURL" : "https://mobile-recharge-a2f5b-default-rtdb.firebaseio.com/",
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage = firebase.storage()

storage = firebase.storage()

# Get the current date and time
current_datetime = timezone.now()

# Get the current date
current_date = current_datetime.date()

# Get the current time
current_time = current_datetime.time()

# Display the current date and time
# print(current_datetime)

# Display the current date
# print(current_date)

# Display the current time
# print(current_time)

indian_ocean_timezone = pytz.timezone('Asia/Kolkata')
current_datetime = datetime.now(indian_ocean_timezone)

def adminlogin(request):
    return render(request , 'AdminLogin.html')

def Index(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == "admin" and password == "admin@123":
        return render(request , 'Add_Plan.html')
    else:
        messages.info(request , 'Your UserName or Password is Wrong')
        return render(request , 'AdminLogin.html')


def add_plan(request):
    Mobile_Operator = request.POST.get('Mobile_Operator')
    Select_Plans   = request.POST.get('Select_Plans')
    Plan_Name      = request.POST.get('Plan_Name')
    Amount         = request.POST.get('Amount')
    Validity      = request.POST.get('Validity')
    SMS           = request.POST.get('SMS')
    Talktime      = request.POST.get('Talktime')
    Data           = request.POST.get('Data')
    Value_Added_Services = request.POST.get('Value_Added_Services')

    data = {"Mobile_Operator" : Mobile_Operator , "Select_Plans" : Select_Plans , "Plan_Name" : Plan_Name,
            "Amount" : Amount  , "Validity" : Validity , "SMS" : SMS ,
            "Talktime" : Talktime , "Data" : Data,
            "Value_Added_Services" : Value_Added_Services}

    database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(Plan_Name).child("Details").set(data)
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    context = {
        "list_data": key,
    }
    return render(request , 'Add_Plan.html',context)

def add_offer(request):
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())

    Mobile_Operator = request.POST.get('Mobile_Operator')
    Offer_Name   = request.POST.get('Offer_Name')
    Offer_Type   = request.POST.get('Offer Type')
    Validity     = request.POST.get('Validity')
    Description  = request.POST.get('Description')

    data = {"Mobile_Operator" : Mobile_Operator , "Offer_Name" : Offer_Name , "Offer_Type" : Offer_Type,
            "Validity" : Validity, "Description" : Description}

    database.child("Admin").child("Operators").child(Mobile_Operator).child("Offers").child(Offer_Name).set(data)
    context = {
        "list_data": key,
    }
    return render(request , 'Add_Offer.html',context)

def add_operator(request):
    Operator_Name = request.POST.get('Mobile_Operator_Name')
    Description   = request.POST.get('Description')
    image1 = request.POST.get('image')
    data = {"Operator_Name" : Operator_Name , "Description" : Description , "Image" : image1}

    database.child("Admin").child("Operators").child(Operator_Name).child("Details").set(data)

    return render(request , 'Add_Operator.html')


def view_operator(request):
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    list_data_dict=[]

    for i in key:
        desc = database.child("Admin").child("Operators").child(i).child("Details").child("Description").get()
        opername = database.child("Admin").child("Operators").child(i).child("Details").child("Operator_Name").get()
        image = database.child("Admin").child("Operators").child(i).child("Details").child("Image").get()
        list_data_dict.append([opername.val() , desc.val(),image.val()])

    context = { 
        "list_data": list_data_dict,
    }

    return render(request, "View_Operator.html", context)

def view_user(request):
    Ans = database.child("Users").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    list_data_dict=[]
    for id in key:
        UserName = database.child("Users").child(id).child("Details").child("UserName").get()
        Mobile_Number = database.child("Users").child(id).child("Details").child("Mobile_Number").get()
        Mobile_Operator_Name = database.child("Users").child(id).child("Details").child("Mobile_Operator").get()
        Email = database.child("Users").child(id).child("Details").child("Email").get()
        Date_Of_Birth = database.child("Users").child(id).child("Details").child("Date_Of_Birth").get()
        Gender = database.child("Users").child(id).child("Details").child("Gender").get()
        list_data_dict.append([id , UserName.val() , Mobile_Number.val(), Mobile_Operator_Name.val(),
                            Email.val() , Date_Of_Birth.val() , Gender.val()])
    
    context = {
        "list_data": list_data_dict,
    }
    return render(request, "View_User.html" , context)
    
def view_transaction(request):
    return render(request , 'View_Transaction.html')

def view_feedback(request):
    Ans = database.child("FeedBack").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    list_data_dict=[]

    for id in key:
        Name = database.child("FeedBack").child(id).child("Name").get()
        Email = database.child("FeedBack").child(id).child("Email").get()
        FeedBack = database.child("FeedBack").child(id).child("Feedback").get()
        Date_Time = database.child("FeedBack").child(id).child("Date_Time").get()
        list_data_dict.append([Name.val() , Email.val(), FeedBack.val(),
                            Date_Time.val()])
    
    context = {
        "list_data": list_data_dict,
    }
    return render(request , 'View_Feedback.html',context)

def logout(request):
    return render(request , 'Logout.html')

def feedback(request):
    return render(request , 'Feedback.html')

def feedback_submit(request):
    Name = request.POST.get('name')
    Email = request.POST.get('email')
    Feedback = request.POST.get('feedback')
    
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    current_date_str = current_date.strftime("%Y-%m-%d")
    current_time_str = current_time.strftime("%H:%M:%S")

    data = {"Name" : Name , "Email" : Email , "Feedback" : Feedback,"Date_Time":current_datetime_str}
    database.child("FeedBack").child(Name).set(data)
    return render(request , 'Feedback.html')

def contactus(request):
    return render(request , 'Contact Us.html')

def contactus_submit(request):
    Name = request.POST.get('name')
    Mobile_Number  = request.POST.get('mobile number')
    Email = request.POST.get('email')
    Subject = request.POST.get('subject')
    Message = request.POST.get('message')
    data = {"Name" : Name , "Mobile_Number" : Mobile_Number , "Email" : Email , "Subject" : Subject , "Message":Message}

    database.child("ContactUs").child(Mobile_Number + '_' + Name).set(data)
    return render(request , 'Contact Us.html')

def aboutus(request):
    return render(request , 'AboutUs.html')

