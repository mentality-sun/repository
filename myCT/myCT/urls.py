"""myCT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from feel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.regist),
    path('regist/',views.regist),
    path('login/',views.login),
    path('index/',views.index),
    path('caidan/',views.caidan),
    path('pay/',views.pay),
    path('tianjia/',views.tianjia),
    # path('fenye/',views.fenye),
    path('tijiao/',views.tijiao),
    path('log/', views.log),
    path('polling/', views.long_polling),
    path('inde/', views.inde),

    path('a/', views.a),
    path('b/', views.b),
    path('c/', views.c),
    path('d/', views.d),
    path('e/', views.e),
    path('f/', views.f),
    path('g/', views.g),
    path('h/', views.h),
    path('house/', views.house),
    path('indexs/', views.indexs),
    path('menu/', views.menu),
    path('fangjian/', views.fangjian),
]
