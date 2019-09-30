"""RGG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import status
from . import spreadsheet
from . import recording
from . import retrieve
from . import upload
from . import updateNumberMappings
from . import startCallFlow
from . import gatherCallFlow
from . import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('views/',views.index) ,
    path('status/' , status.isOpen) ,
    path('spreadsheet/' , spreadsheet.getRelation) ,
    path('recording/' , recording.getFile) ,
    path('retrieve/' , retrieve.retrieve) ,
    path('upload/' , upload.upload) ,
    path('getRecording/' , recording.getCurrentlyUploadedRecordings) ,
    path('deleteRecording/' , recording.deleteRecording) ,
    path('getSpreadsheet/' , spreadsheet.getCurrentlyUploadedSpreadsheets) ,
    path('deleteSpreadsheet/' , spreadsheet.deleteSpreadsheet) ,
    path('updateHours/' , status.update) ,
    path('getHoursOfOperation/' , status.getHoursOfOperation) ,
    path('getNumberMappings/' , updateNumberMappings.getNumberMappings) ,
    path('updateNumberMappings/' , updateNumberMappings.update) ,
    path('start/' , startCallFlow.start) ,
    path('gather/' , gatherCallFlow.main) ,
    path('dyk/' , gatherCallFlow.dyk ) ,
    path('login/' , auth.logIn) ,
    path('authenticated/' , auth.isAuthenticated)


]
