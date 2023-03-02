"""encryptiongw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from encryptiongw import api 
from encryptiongw import views
#from encryptiongw import models

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/encrypt-data/(?P<apikey>.+)/$', api.encrypt_data),
    re_path(r'^api/get-encrypted-data/(?P<apikey>.+)/$', api.get_encrypt_data),
    re_path(r'^api/update-device/$', api.update_device),
    re_path(r'^private-media/qrcode/(?P<file_id>\d+)-file.(?P<extension>\w\w\w)$', views.getAppFile, name='view_private_file'),
]



