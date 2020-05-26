"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

# Group 8 CCC Assignment2
# Authors: Jiawei Wu 1036192, Luxi Li 1017820, Lixian Sun 938295, Deng Pan 354059, Rui Wang 978296
# Date: 26/05/2020
# Description: Backend of the web application, read and process data from couchdb.

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('location', views.pong),
    path('heatorigin', views.heatMapOrigin),
    path('heatbystate', views.heatByState),
    path('language', views.language),
    path('index', views.index),
    path('daytime', views.dayAndTime),
    path('test', views.test)

]
