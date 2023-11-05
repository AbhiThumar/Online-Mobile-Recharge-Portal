from django.shortcuts import render
from django.contrib import auth 
import pyrebase
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from django.http import HttpResponse, JsonResponse 

import io
from PIL import Image

import firebase_admin
from firebase_admin import db

from django.core.files.base import File
from django.db import models


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

# for update the database entry 
# #Let's say you want to update the Name of the operator 
#database.child("Admin").child("Operators").child("Airtel").child("Details").update({"Operator_Name" : "Airtel"})

# for update data in multiple locations at the same time 
# data = {"Admin/Operators/Airtel/Details" : {"Operator_Name" : "Hello"} ,
#         "Admin/Operators/Jio/Details" : {"Operator_Name" : "oppo"} }
# database.update(data)

# To fetch the data from database 
# v = database.child("Users").child("7383200527_Jay_Vakhariya").get()
# for det in v.each():
#     print(det.key())
#     print(det.val()) 

# To delete the data from the database 
# v = database.child("Users").child("7383200527_Jay_Vakhariya").remove()

# To Fetch the data from the Firebase
# Ans = database.child("Users").get()
# print(Ans.val())

# To Fetch the data from the Firebase for the particular user 
# Ans = database.child("Users").get()
# for det in Ans.each():
#     print(det.key())
#     print(det.val())
# print(Ans.val())

# For fetch only keys 
# vi = database.child("Admin").child("Operators").shallow().get()
# print(vi.val())


# storage.child("logo.png").put("E:/Mobile_Operators_Logo/Vodafone.jpg")
# storage.download("logo.png" , "logos.png")

# storage.child("logo.png").put("E:/Mobile_Operators_Logo/Vodafone.jpg")

def index(request):
    return render(request , 'index.html')

def postsign(request):
    if request.method == 'POST':
        return render(request , "welcome.html")

def logout(request):
    auth.logout(request)
    return render(request , 'signup.html')

def signup(request):
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    context = {
        "list_data": key,
    }
    return render(request,'signup.html',context)


def postsignup(request):
    Name = request.POST.get('name')
    mobile = request.POST.get('mobile')
    Mobile_Operator_Name = request.POST.get('Mobile_Operator')
    email = request.POST.get('email')
    date = request.POST.get('Date_Of_Birth')
    Gender = request.POST.get('gender')
    address = request.POST.get('Address')

    data={"Name" : Name ,"Mobile_Number" : mobile ,"Mobile_Operator_Name" : Mobile_Operator_Name,"Gender" : Gender,
         "Email" : email , "Date_Of_Birth":date , "Address":address}

    database.child("Users").child(mobile+ '_' + Name).child("Details").set(data)

    return render(request , 'index.html')


def add_operator(request):
    Operator_Name = request.POST.get('Mobile_Operator_Name')
    Description   = request.POST.get('Description')
    image1 = request.POST.get('image')
    data = {"Operator_Name" : Operator_Name , "Description" : Description , "Image" : image1}

    database.child("Admin").child("Operators").child(Operator_Name).child("Details").set(data)

    return render(request , 'Add_Operator.html')



def try1(request):
    return render(request , 'try_1.html')

def add_plan(request):
    Mobile_Operator = request.POST.get('Mobile_Operator')
    Select_Plans   = request.POST.get('Select_Plans')
    Plan_Name      = request.POST.get('Plan_Name')
    Amount         = request.POST.get('Amount')
    Validity      = request.POST.get('Validity')
    SMS           = request.POST.get('SMS')
    Talktime      = request.POST.get('Talktime')
    Full_Talktime  = request.POST.get('Full_Talktime')
    Data           = request.POST.get('Data')
    Value_Added_Services = request.POST.get('Value_Added_Services')

    data = {"Mobile_Operator" : Mobile_Operator , "Select_Plans" : Select_Plans , "Plan_Name" : Plan_Name,
            "Amount" : Amount  , "Validity" : Validity , "SMS" : SMS ,
            "Talktime" : Talktime , "Full_Talktime" :  Full_Talktime , "Data" : Data,
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
            print(det.key())
            key.append(det.key())
    list_data_dict=[]
    for id in key:
        Name = database.child("Users").child(id).child("Details").child("Name").get()
        Mobile_Number = database.child("Users").child(id).child("Details").child("Mobile_Number").get()
        Mobile_Operator_Name = database.child("Users").child(id).child("Details").child("Mobile_Operator_Name").get()
        Email = database.child("Users").child(id).child("Details").child("Email").get()
        Date_Of_Birth = database.child("Users").child(id).child("Details").child("Date_Of_Birth").get()
        Gender = database.child("Users").child(id).child("Details").child("Gender").get()
        Address = database.child("Users").child(id).child("Details").child("Address").get()
        list_data_dict.append([id , Name.val() , Mobile_Number.val(), Mobile_Operator_Name.val(),
                            Email.val() , Date_Of_Birth.val() , Gender.val(), Address.val()])
    
    context = {
        "list_data": list_data_dict,
    }
    return render(request, "View_User.html" , context)

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