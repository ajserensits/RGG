import xlrd
import random
import os
from datetime import datetime
from pytz import timezone
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from . import recording
from . import spreadsheet
from . import auth
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


@csrf_exempt
def upload(request):
    user = request.GET.get('user')
    token = request.GET.get('token')

    if auth.isAuthenticatedBool(user , token) == False:
        return HttpResponseRedirect('/static/login.html?user=' + user + '&token=' + token)
    file_type = request.GET.get('file_type')
    file_name = request.POST.get('file_to_replace')
    file_data = request.FILES['data']
    fs = FileSystemStorage()
    MEDIA_ROOT = fs.location
    fs.location = MEDIA_ROOT + "/" + file_type
    BASE_URL = fs.base_url
    fs.base_url = BASE_URL = "/" + file_type
    os.remove(fs.location + "/" + file_name)
    fs.save(file_name, file_data)
    return HttpResponseRedirect('/static/admin.html?upload_status=success&type=' + file_type + '&user=' + user + '&token=' + token)