"""lineProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from linebotApp import views
from django.urls import include, re_path
urlpatterns = [
    re_path('^callback', views.callback),
    re_path(r'^select_job/(?P<id>\w+)/$', views.select_job, name='select_job'),
    re_path(r'^update_job/(?P<lineId>\w+)/(?P<id>\w+)/$', views.update_job, name='update_job'),
    re_path(r'^selectCompany/(?P<id>\w+)/$',
            views.selectCompany, name='selectCompany'),
    re_path(r'^updateCompany/(?P<lineId>\w+)/(?P<id>\w+)/$',
            views.update_Company, name='update_Company'),
    path('admin/', admin.site.urls),
]
