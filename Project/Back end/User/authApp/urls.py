from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    path('',views.home,name="home"),
    path('registration/',views.Registration, name="Registration"),
    path('registration/otp/',views.otpRegistration, name="otp-Registration"),
    path('login/',views.userLogin, name="user-login"),
    path('login/otp/',views.otpLogin, name="otp-login"),
    path('logout/',auth_view.LogoutView.as_view(template_name='logout.html')),
    path('recharge_now',views.recharge_now,name='recharge_now'),
    path('plans',views.plans,name='plans'),
    path('offers',views.offers,name='offers'),
    path('offs',views.offs,name='offs'), 
      path('transaction',views.mytrans,name='mytrans'),
    
]