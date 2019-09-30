import xlrd
import random
import json
from datetime import datetime
from pytz import timezone
from django.http import HttpResponse
from . import auth
from . import settings



def update(request):
    open_time = request.GET.get('open')
    close_time = request.GET.get('closed')
    user = request.GET.get('user')
    token = request.GET.get('token')

    if auth.isAuthenticatedBool(user , token) == False:
        return auth.isAuthenticated(user , token)

    data = {}
    data["open"] = open_time
    data["closed"] = close_time

    data = json.dumps(data)

    file = open(settings.HOURS_OF_OPERATION_URL, "w")
    file.write(data)
    file.close()

    return HttpResponse('{"Status" : "Success" , "open" : "' + open_time + '" , "closed" : "' + close_time + '"}' , content_type="application/json")

def getHoursOfOperation(request):
    json_data = open(settings.HOURS_OF_OPERATION_URL)
    data = json.load(json_data)
    response_data = '{"open" : "' + data["open"] + '" , "closed" : "' + data["closed"] + '"}'

    return HttpResponse(response_data , content_type="application/json")



def isOpen(request):
    tz = timezone('US/Eastern')
    time_str = str(datetime.now(tz))

    time_arr = time_str.split(' ')
    time = time_arr[1].split(':')
    hours = time[0]
    minutes = time[1]

    full_date = get_full_date()
    full_time = get_full_time()

    json_data = open(settings.HOURS_OF_OPERATION_URL)
    data = json.load(json_data)
    open_hour = int(data["open"])
    closed_hour = int(data["closed"])
    hours = int(hours)

    if hours >= open_hour and hours <= closed_hour:
        return HttpResponse('{"status" : "true" , "date" : "' + full_date + '" , "time" : "' + full_time + '"}' , content_type="application/json")
    else:
        return HttpResponse('{"status" : "false" , "date" : "' + full_date + '" , "time" : "' + full_time + '"}' , content_type="application/json")

def isItOpen():
    tz = timezone('US/Eastern')
    time_str = str(datetime.now(tz))

    time_arr = time_str.split(' ')
    time = time_arr[1].split(':')
    hours = time[0]
    #minutes = time[1]

    json_data = open(settings.HOURS_OF_OPERATION_URL)
    data = json.load(json_data)
    open_hour = int(data["open"])
    closed_hour = int(data["closed"])
    hours = int(hours)

    if hours >= open_hour and hours <= closed_hour:
        return "true"
    else:
        return "false"


def get_full_time():
    tz = timezone('US/Eastern')
    time_str = str(datetime.now(tz))

    time_arr = time_str.split(' ')
    time = time_arr[1].split(':')
    hours = time[0]
    minutes = time[1]


    minutes = int(minutes)
    if minutes < 30:
        minutes = "00"
    else:
        minutes = "30"

    full_time_str = hours + minutes

    return full_time_str
    ## this returns a datetime object pointing to right now
    ## according to the timezone info object handed in as the tz variable.


def get_full_date():
    tz = timezone('US/Eastern')
    time_str = str(datetime.now(tz))

    time_arr = time_str.split(' ')
    date = time_arr[0].split('-')

    year = date[0]
    month = date[1]
    day = date[2]

    if day[0] == "0":
        day = day[1]

    if month[0] == "0":
        month = month[1]

    #year = year[2] + year[3]


    full_date_str = month + "/" + day + "/" + year
    return full_date_str
    ## this returns a datetime object pointing to right now
    ## according to the timezone info object handed in as the tz variable.










