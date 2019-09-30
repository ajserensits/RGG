import xlrd
import random
from datetime import datetime
from pytz import timezone
from django.http import HttpResponse
from . import recording
from . import spreadsheet

def retrieve(request):
    file_type = request.GET.get('file_type')
    file_name = request.GET.get('file_name')

    if file_type != "spreadsheet" and file_type != "mp3":
        return HttpResponse('{"Status" : "Failed" , "Error" : "INVALID_FILE_TYPE"}' , content_type="application/json")

    if file_name == None or file_name == "":
        return HttpResponse('{"Status" : "Failed" , "Error" : "INVALID_FILE_NAME"}' , content_type="application/json")

    if file_type == "spreadsheet":
        return spreadsheet.getFileFromName(file_name)

    if file_type == "mp3":
        return recording.getFileFromName(file_name)

