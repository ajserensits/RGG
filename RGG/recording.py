"""
 Author: Andrew Serensits [ ajserensits@avaya.com ]

 This file is meant to handle listing all current recordings as well as delete recordings
"""

from django.http import HttpResponse
import json
import os
from os import listdir
from os.path import isfile, join


"""
 This function gives you all of the recording names in /media/recordings/

 @param HttpRequest
 @return HttpResponse of type application/json containing all of the recording file names
"""
def getCurrentlyUploadedRecordings(request):
    files = listdir("RGG/media/recordings/")
    json_data = json.dumps(files)
    return HttpResponse(json_data, content_type="application/json")

"""
 This function allows you to delete a recording from /media/recordings/

 @param HttpRequest with a GET parameter as the file_name to delete
 @return HttpResponse of type application/json indicating whether or not the file was successfully deleted 
"""
def deleteRecording(request):
    fileName = request.GET.get('file_name')
    os.remove('RGG/media/recordings/' + fileName)
    return HttpResponse('{"Status" : "Success"}', content_type="application/json")
