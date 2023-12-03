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
import random   
from firebase_admin import db

from django.core.files.base import File
from django.db import models
from django.utils import timezone

from firebase_admin import firestore
from firebase_admin import messaging
from .models import OTP

from django.conf import settings
from firebase_admin import credentials
from firebase_admin import messaging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
import random
import string
import smtplib

from django.core.mail import send_mail
from datetime import datetime
from reportlab.pdfgen import canvas

config={
	"apiKey": "AIzaSyBOSZKBZQYdcHmaCs5nlOhrD9GGVuiVRFU",
    "authDomain": "mobile-recharge-a2f5b.firebaseapp.com",
    "projectId": "mobile-recharge-a2f5b",
    "storageBucket": "mobile-recharge-a2f5b.appspot.com",
    "messagingSenderId": "220946121042",
    "appId": "1:220946121042:web:402e08cd8a20f377ecba8b",
    "measurementId": "G-6JZEK2YC24",
    #"serviceAccount" : "D:/Academics/DA-IICT/Semester-5/Software Engineering/project/final_project/serviceAccount.json",
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

indian_ocean_timezone = pytz.timezone('Asia/Kolkata')
current_datetime = datetime.now(indian_ocean_timezone)
# print(current_datetime)
# print(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
# print(a)

# Get the current UTC time
utc_now = datetime.utcnow()

# Set the UTC timezone
# utc_timezone = pytz.timezone('UTC')
# utc_now = utc_timezone.localize(utc_now)

# Convert to Indian Standard Time (IST)
# ist_timezone = pytz.timezone('Asia/Kolkata')
# ist_now = utc_now.astimezone(ist_timezone)

# Print the current date and time in IST
# print("Current Date and Time (IST):", ist_now.strftime("%Y-%m-%d %H:%M:%S"))

def fiber(request):
    return render(request , 'index.html')

def adminlogin(request):
    return render(request , 'AdminLogin.html')

def Index(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == "admin" and password == "Admin@123":
        return render(request , 'admin_dashboard.html')
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
        Age = database.child("Users").child(id).child("Details").child("Age").get()
        list_data_dict.append([id , UserName.val() , Mobile_Number.val(), Mobile_Operator_Name.val(),
                            Email.val() , Date_Of_Birth.val() , Gender.val() , Age.val()])
    
    context = {
        "list_data": list_data_dict,
    }
    return render(request, "View_User.html" , context)

    
def view_transaction(request):
    Ans = database.child("Transaction").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    list_data_dict=[]
    for id in key:
        Transaction_Id = database.child("Transaction").child(id).child("Transaction_Id").get()
        User_Id = database.child("Transaction").child(id).child("User_Id").get()
        Date_Time = database.child("Transaction").child(id).child("Date & Time").get()
        Mobile_Operator = database.child("Transaction").child(id).child("Mobile_Operator").get()
        Select_Plans = database.child("Transaction").child(id).child("Select_Plans").get()
        PlanName = database.child("Transaction").child(id).child("PlanName").get()
        Amount = database.child("Transaction").child(id).child("Amount").get()
        list_data_dict.append([Transaction_Id.val() , User_Id.val() , Date_Time.val() ,Mobile_Operator.val(),
                                Select_Plans.val() ,PlanName.val() , Amount.val()])
    
    context = {
        "list_data": list_data_dict,
    }
    return render(request , 'View_Transaction.html',context)

def user_transaction(request):
    email = request.session.get('email')
    listid = database.child("Users").get()
    key=[]
    for det in listid.each():
                    key.append(det.key())
         
    for id in key:
                    Email = database.child("Users").child(id).child("Details").child("Email").get()
                    if Email.val() == email: 
                        uid = database.child("Users").child(id).child("Details").child("User_Id").get()
                        User_Id = uid.val()
                        break
    
    transaction_id = database.child("Transaction").get()
    key1=[]
    answer=[]
    for det in transaction_id.each():
                    key1.append(det.key())
    for id in key1:
                    userid = database.child("Transaction").child(id).child("User_Id").get()
                    if userid.val() == User_Id: 
                       answer.append(id)

    list_data_dict=[]
    for id in answer:
        Transaction_Id = database.child("Transaction").child(id).child("Transaction_Id").get()
        Date_Time = database.child("Transaction").child(id).child("Date & Time").get()
        Mobile_Operator = database.child("Transaction").child(id).child("Mobile_Operator").get()
        Select_Plans = database.child("Transaction").child(id).child("Select_Plans").get()
        PlanName = database.child("Transaction").child(id).child("PlanName").get()
        Amount = database.child("Transaction").child(id).child("Amount").get()
        list_data_dict.append([Transaction_Id.val() ,Date_Time.val(), Mobile_Operator.val(),
                                Select_Plans.val() ,PlanName.val() , Amount.val()])
    
    context = {
        "list_data": list_data_dict,
    }

    return render(request ,'User_Transaction.html',context)


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
    
    Date_Time = current_datetime

    data = {"Name" : Name , "Email" : Email , "Feedback" : Feedback,"Date_Time":Date_Time}
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

    # Subject
    subject = 'User Inquiry: Contacting Fiber Support'

    # Body
    body = """Dear Fiber Support Team,

    I hope this message finds you well. My name is [User's Name], and I am reaching out to you regarding the following matter:

    [User's Message or Inquiry]

    Please review and address my inquiry at your earliest convenience. I appreciate your prompt assistance in this matter.

    Thank you for your time and attention.

    Best regards,
    [User's Name]
    [User's Contact Information]
    """

    send_mail(subject, body, [settings.EMAIL_HOST_USER],Email, fail_silently=False)

    return render(request , 'Contact Us.html')

def aboutus(request):
    return render(request , 'AboutUs.html')

def profile(request):
    return render(request , 'profile.html')

def profile_edit(request):
    return render(request , 'profile.html')

def recharge(request):
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    context = {
        "list_data": key,
    }
    return render(request , 'Recharge_Now.html',context)

def show_plans(request):
    Mobile_Number = request.POST.get('Mobile_Operator')
    Mobile_Operator = request.POST.get('Mobile_Operator')
    Select_Plans  = request.POST.get('Select_Plans')

    request.session['Mobile_Number'] = Mobile_Number
    request.session['Mobile_Operator'] = Mobile_Operator
    request.session['Select_Plans'] = Select_Plans

    Ans = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).get()
    
    key=[]
    for det in Ans.each():
            key.append(det.key())
    list_data_dict=[]

    for id in key:
        Plan_Name = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Plan_Name").get()
        Data = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Data").get()
        Price = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Amount").get()
        SMS = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("SMS").get()
        Talktime = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Talktime").get()
        Validity = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Validity").get()
        Value_Added_Services = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(id).child("Details").child("Value_Added_Services").get()
        list_data_dict.append([ Plan_Name.val() , Data.val() , Price.val(), SMS.val(),Talktime.val(),Validity.val(),Value_Added_Services.val()])

    context = {
        "Mobile_Operator":Mobile_Operator, "Select_Plans":Select_Plans, "list_data": list_data_dict,
    }

    
    return render(request , 'Show_Plans.html',context)

def payment(request):
    PlanName = request.GET.get('PlanName')

    request.session['PlanName'] = PlanName

    # param1 = request.GET.get('param1')
    # Validity = request.GET.get('Validity')
    # Data = request.GET.get('Data')
    # context = {
    #     "Price" : Price , "param1" : param1 ,"Validity" : Validity , "Data" : Data , 
    #    }

    context = {
        "PlanName" : PlanName,
       }
    return render(request , 'Payment.html' , context ) 

def gen_transaction_id():
    id = str(random.randint(100000000000, 999999999999))
    return id


def pay(request):
    tran_id = gen_transaction_id()
    Date_Time = current_datetime
    PlanName = request.session.get('PlanName')
    Mobile_Number = request.session.get('Mobile_Number')
    Mobile_Operator = request.session.get('Mobile_Operator')
    Select_Plans = request.session.get('Select_Plans')
    email = request.session.get('email')
    today = datetime.now()
    
    listid = database.child("Users").get()
    key=[]
    for det in listid.each():
                    key.append(det.key())


            
    for id in key:
                    Email = database.child("Users").child(id).child("Details").child("Email").get()
                    if Email.val() == email: 
                        FullName = database.child("Users").child(id).child("Details").child("FullName").get()
                        FullName = FullName.val()
                        uid = database.child("Users").child(id).child("Details").child("User_Id").get()
                        User_Id = uid.val()
                        break
    
    list_data_dict = []

    Data = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(PlanName).child("Details").child("Data").get()
    Amount = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(PlanName).child("Details").child("Amount").get()
    SMS = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(PlanName).child("Details").child("SMS").get()
    Talktime = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(PlanName).child("Details").child(" Talktime").get()
    Validity = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(PlanName).child("Details").child("Validity").get()
    Value_Added_Services = database.child("Admin").child("Operators").child(Mobile_Operator).child("Plans").child(Select_Plans).child(PlanName).child("Details").child("Value_Added_Services").get()
    
    list_data_dict.append([ tran_id , User_Id, Date_Time, email, Mobile_Operator , Select_Plans , PlanName, Data.val() , Amount.val(), SMS.val(),Validity.val(),Value_Added_Services.val()])
    price = Amount.val()
    # Subject
    subject = 'Payment Successful! Thank You for Choosing Fiber'

    # Body
    body = """Dear {FullName},

    We are delighted to inform you that your payment on Fiber was successful! Your transaction details are as follows:

    Transaction ID: { tran_id }
    Amount Paid:    {price}
    Date:           {Date_Time}

    Thank you for choosing Fiber for your Mobile Recharge. We appreciate your business!

    If you have any questions or concerns regarding your payment, feel free to reach out to our support team at [settings.EMAIL_HOST_USER].

    Best regards,
    The Fiber Team
    """

    # send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    context = {
            "Mobile_Number" : Mobile_Number,"list_data":list_data_dict,
       }


    data = {"Transaction_Id" : tran_id , "User_Id" : User_Id , "Date & Time" : Date_Time,"Mobile_Operator":Mobile_Operator,"Select_Plans":Select_Plans,"PlanName":PlanName,"Amount":price  }

    database.child("Transaction").child(tran_id).set(data)
   
    return render(request , 'Message.html',context)

def debitcard(request):
     return render(request , 'Debitcard.html')
    
def creditcard(request):
     return render(request , 'Creditcard.html')

def user_reg(request):
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
                key.append(det.key())
    context = { "list_data": key,}
    return render(request , 'reg.html',context)


def calculate_age(birth_date):
    try:
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
        today = datetime.now()

        print("Birth Date:", birth_date)
        print("Today:", today)

        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        print("Calculated Age:", age)

        return age

    except Exception as e:
        print("Error in calculate_age:", e)
        return 0

def generate_user_id():
    # Generate 3 random alphabetic characters
    alpha_part = ''.join(random.choices(string.ascii_uppercase, k=3))
    
    # Generate 5 random numeric characters
    numeric_part = ''.join(random.choices(string.digits, k=5))
    
    # Combine alpha and numeric parts to form the user ID
    user_id = alpha_part + numeric_part
    
    return user_id

def reg(request):
    if request.method == 'POST':
            User_id = generate_user_id()    
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            Mobile_Operator= request.POST.get('Mobile_Operator')
            Date_Of_Birth = request.POST.get('Date_Of_Birth')
            gender = request.POST.get('gender')
            user_age = calculate_age(Date_Of_Birth)

            Userid = database.child("Users").get()
            key=[]
            for det in Userid.each():
                                key.append(det.key())
            
            for id in key:
                    Email = database.child("Users").child(id).child("Details").child("Email").get()
                    if Email.val() == email: 
                       message = "Email is already registered. Please use a different email or log in with your existing account."
                       return render(request , 'reg.html',{'message': message})



            data={"User_Id" : User_id , "FullName" : fullname , "Email" : email , "Mobile_Number" : phone_number , "Mobile_Operator" : Mobile_Operator, "Date_Of_Birth" : Date_Of_Birth,"Age" : user_age , "Gender" : gender}
            database.child("Users").child(phone_number).child("Details").set(data)

            # Subject
            subject = 'Welcome to Fiber! Your Registration is Successful'

            # Body
            body = f"""Dear New User,

            Welcome to Fiber! We're thrilled to have you as part of our community. Your registration is now complete, and you are all set to explore everything Fiber has to offer.

            Here are your registration details:
            User Id:         {User_id}
            Phone Number:    {phone_number}
            Fullname:        {fullname}
            Email:           {email}
            Mobile_Operator: {Mobile_Operator}
            Gender:          {gender}
            User Age:        {user_age}

            Feel free to log in to your account and start enjoying the features of Fiber. If you have any questions or need assistance, our support team is here to help.

            Thank you for choosing Fiber! We look forward to serving you.

            Best regards,   
            The Fiber Team
            """

            send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            return render(request , 'SignIn.html')
    else:   
        return render(request , 'SignIn.html')

# # Generate a random 6-digit OTP
def generate_otp():
    otp = str(random.randint(100000, 999999))
    return otp

def otp(request):
        email = request.POST.get('email')
        Userid = database.child("Users").get()
        key=[]
        for det in Userid.each():
                        key.append(det.key())
    
        for id in key:
            Email = database.child("Users").child(id).child("Details").child("Email").get()
            if Email.val() == email:   
                otp_code = generate_otp()
                subject = 'Your OTP for Fiber Login'

                # Body
                body = f"""Dear User,

                You have requested a one-time password (OTP) to log into your Fiber account.

                Your OTP is: {otp_code}

                Please use this code to complete the login process. Note that this code is valid for a short period and should not be shared with anyone.

                If you did not request this OTP, please disregard this email.

                Thank you for choosing Fiber.

                Best regards,
                The Fiber Team
                """
            
                send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            
                messages.success(request, 'OTP sent successfully!')


                User_Id = database.child("Users").child(id).child("Details").child("User_Id").get()
                request.session['otp'] = otp_code
                request.session['email'] = email
                request.session['User_Id'] = User_Id

                
                return render(request, 'OTP_Enter.html')

        message = "Email not found. Please register yourself first."
        return render(request, 'SignIn.html', {'message': message})

def resend_otp(request):
        email =  request.session.get('email')
        otp_code = generate_otp()
        subject = 'Your OTP for Fiber Login'

        # Body
        body = f"""Dear User,

        You have requested a one-time password (OTP) to log into your Fiber account.

        Your OTP is: {otp_code}

        Please use this code to complete the login process. Note that this code is valid for a short period and should not be shared with anyone.

        If you did not request this OTP, please disregard this email.

        Thank you for choosing Fiber.

        Best regards,
        The Fiber Team
        """
       
        send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    
        messages.success(request, 'OTP sent successfully!')

        request.session['otp'] = otp_code
        request.session['email'] = email

        return render(request, 'OTP_Enter.html')

def dashboard(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if user_otp == stored_otp:
            messages.success(request, 'OTP verification successful!')
            return render(request, 'User_Dashboard.html')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'OTP_Enter.html') 
    else:
         return render(request, 'User_Dashboard.html')
    

def generate_pdf(user_info, file_name='user_information.pdf'):
    # Create a PDF document
    pdf_canvas = canvas.Canvas(file_name)

    # Add content to the PDF
    pdf_canvas.drawString(100, 800, 'User Information:')
    pdf_canvas.drawString(100, 780, f"Name: {user_info.get('name', 'N/A')}")
    pdf_canvas.drawString(100, 760, f"Email: {user_info.get('email', 'N/A')}")
    pdf_canvas.drawString(100, 740, f"Birth Date: {user_info.get('birth_date', 'N/A')}")
    
    if 'birth_date' in user_info:
        age = calculate_age(user_info['birth_date'])
        pdf_canvas.drawString(100, 720, f"Age: {age} years")

    # Save the PDF
    pdf_canvas.save()

def userprofile(request):
    email =  request.session.get('email')
    Userid = database.child("Users").get()
    key=[]
    for det in Userid.each():
                key.append(det.key())
        
    profile=[]

    for id in key:
            Email = database.child("Users").child(id).child("Details").child("Email").get()
            print(Email.val())
            if Email.val() == email:
                    FullName = database.child("Users").child(id).child("Details").child("FullName").get()
                    Mobile_Number = database.child("Users").child(id).child("Details").child("Mobile_Number").get()
                    Mobile_Operator_Name = database.child("Users").child(id).child("Details").child("Mobile_Operator").get()
                    Email = database.child("Users").child(id).child("Details").child("Email").get()
                    Date_Of_Birth = database.child("Users").child(id).child("Details").child("Date_Of_Birth").get()
                    Gender = database.child("Users").child(id).child("Details").child("Gender").get()
                    Age = database.child("Users").child(id).child("Details").child("Age").get()
                    profile.append([FullName.val() , Mobile_Number.val(), Mobile_Operator_Name.val(),
                                        Email.val() , Date_Of_Birth.val() , Gender.val() , Age.val()])
                    break

    context = {"list_data" : profile,}
    return render(request, 'Profile.html',context)

def offers(request):
    Ans = database.child("Admin").child("Operators").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    context = {
        "list_data": key,
    }
    return render(request, 'Offer.html',context)

def view_offers(request):
    operator = request.POST.get('Mobile_Operator')
    Ans =  database.child("Admin").child("Operators").child(operator).child("Offers").get()
    key=[]
    for det in Ans.each():
            key.append(det.key())
    print(key)
    list_data_dict=[]
    for id in key:
        Description = database.child("Admin").child("Operators").child(operator).child("Offers").child(id).child("Description").get()
        Offer_Name = database.child("Admin").child("Operators").child(operator).child("Offers").child(id).child("Offer_Name").get()
        Mobile_Operator = database.child("Admin").child("Operators").child(operator).child("Offers").child(id).child("Mobile_Operator").get()
        Offer_Type = database.child("Admin").child("Operators").child(operator).child("Offers").child(id).child("Offer_Type").get()
        Validity = database.child("Admin").child("Operators").child(operator).child("Offers").child(id).child("Validity").get()
        
        list_data_dict.append([ Description.val() , Offer_Name.val(), Mobile_Operator.val(), Offer_Type.val() ,  Validity.val()])
    context = {
         "list_data": list_data_dict,
    }
    return render(request, 'V_offers.html',context)



