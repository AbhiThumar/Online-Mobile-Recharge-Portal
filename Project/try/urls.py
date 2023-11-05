"""
URL configuration for try project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('postsign',views.postsign),
    path('logout',views.logout,name='log'),
    path('signup',views.signup,name='signup'),
    path('postsignup',views.postsignup,name='postsignup'),
    path('add_operator',views.add_operator,name='add_operator'),
    path('add_plan',views.add_plan,name='add_plan'),
    path('add_offer',views.add_offer,name='add_offer'),
    path('view_operator',views.view_operator,name='view_operator'),
    path('view_user',views.view_user,name='view_user'),
    path('recharge_now',views.recharge_now,name='recharge_now'),
    path('plans',views.plans,name='plans'),
    path('offers',views.offers,name='offers'),
    path('offs',views.offs,name='offs'), 
]   