from django.urls import path,include
from . import views
from adminApp.templates import *
from django.contrib.auth import views as auth_view
from adminApp.views import *
# from django.views.generic import TemplateView

urlpatterns = [
    path('', views.adminlogin,name='adminlogin'),
    path('Index', views.Index,name='Index'),
    path('add_operator',views.add_operator,name='add_operator'),
    path('add_plan',views.add_plan,name='add_plan'),
    path('add_offer',views.add_offer,name='add_offer'),
    path('view_operator',views.view_operator,name='view_operator'),
    path('view_user',views.view_user,name='view_user'),
    path('view_transaction',views.view_transaction,name='view_transaction'),
    path('view_feedback',views.view_feedback,name='view_feedback'),
    path('logout',views.logout,name='logout'),

    path('feedback' , views.feedback , name='feedback'),
    path('feedback_submit' , views.feedback_submit , name='feedback_submit'),
    path('contactus' , views.contactus , name='contactus'),
    path('contactus_submit' , views.contactus_submit , name='contactus_submit'),
    path('aboutus' , views.aboutus, name='aboutus'),
]   