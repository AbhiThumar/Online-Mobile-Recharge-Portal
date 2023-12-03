from django.urls import path,include
from . import views
from adminApp.templates import *
from django.contrib.auth import views as auth_view
from adminApp.views import *
# from django.views.generic import TemplateView

urlpatterns = [
    #admin side
    path('', views.fiber,name='fiber'),
    path('adminlogin', views.adminlogin,name='adminlogin'),
    path('Index', views.Index,name='Index'),
    path('add_operator',views.add_operator,name='add_operator'),
    path('add_plan',views.add_plan,name='add_plan'),
    path('add_offer',views.add_offer,name='add_offer'),
    path('view_operator',views.view_operator,name='view_operator'),
    path('view_user',views.view_user,name='view_user'),
    path('view_transaction',views.view_transaction,name='view_transaction'),
    path('view_feedback',views.view_feedback,name='view_feedback'),
    path('logout',views.logout,name='logout'),

    #user side
    path('feedback' , views.feedback , name='feedback'),
    path('feedback_submit' , views.feedback_submit , name='feedback_submit'),
    path('contactus' , views.contactus , name='contactus'),
    path('contactus_submit' , views.contactus_submit , name='contactus_submit'),
    path('aboutus' , views.aboutus, name='aboutus'),
    path('recharge' , views.recharge , name='recharge'),
    path('show_plans' , views.show_plans , name='show_plans'),
    path('payment' , views.payment, name='payment'),
    path('pay', views.pay, name='pay'),
    path('debitcard' , views.debitcard , name='debitcard'),
    path('creditcard' , views.creditcard , name='creditcard'),
    path('user_reg',views.user_reg,name='user_reg'),
    path('reg',views.reg,name='reg'),
    path('otp',views.otp,name='otp'),
    path('resend_otp',views.resend_otp,name='resend_otp'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('userprofile' , views.userprofile , name='userprofile'),
    path('offers' , views.offers , name='offers'),
    path('view_offers' , views.view_offers , name='view_offers'),
    path('user_transaction' , views.user_transaction , name='user_transaction'),

    
]   