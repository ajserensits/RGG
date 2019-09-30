from django.http import HttpResponse
import json
import os
from os import listdir
from os.path import isfile, join


def getCurrentlyUploadedRecordings(request):
    files = listdir("RGG/media/recordings/")
    json_data = json.dumps(files)
    return HttpResponse(json_data, content_type="application/json")

def deleteRecording(request):
    fileName = request.GET.get('file_name')
    os.remove('RGG/media/recordings/' + fileName)
    return HttpResponse('{"Status" : "Success"}', content_type="application/json")


def getFile(request):
    fileName = request.GET.get('file_name')
    # your other codes ...
    file = open("RGG/media/" + fileName + ".mp3", "rb").read()
    #response['Content-Disposition'] = 'attachment; filename=filename.mp3'
    return HttpResponse(file, content_type="audio/mpeg")


def getFileFromName(name):
    # your other codes ...
    file = open("RGG/media/" + name + ".mp3", "rb").read()
    response =  HttpResponse(file, content_type="audio/mpeg")
    response['Content-Disposition'] = 'attachment; filename=' + name + '.mp3'
    return response

def uploadFile(fileData , fileName):
    # your other codes ...
    file = open("RGG/media/" + fileName + ".mp3", "w")
    file.write(fileData)
    file.close()

    response = HttpResponse('{"Status" : "Success"}', content_type="application/json")
    return response


def testGetFile():
    fileName = "RLL_Menu"
    # your other codes ...
    file = open("RGG/media/" + fileName + ".mp3", "rb").read()
    #response['Content-Disposition'] = 'attachment; filename=filename.mp3'
