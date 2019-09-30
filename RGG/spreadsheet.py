import xlrd
import random
import json
from datetime import datetime
from pytz import timezone
from django.http import HttpResponse
import os
from os import listdir
from os.path import isfile, join
from . import settings


def getCurrentlyUploadedSpreadsheets(request):
    files = listdir(settings.SPREADSHEETS_URL)
    json_data = json.dumps(files)
    return HttpResponse(json_data, content_type="application/json")

def deleteSpreadsheet(request):
    fileName = request.GET.get('file_name')
    os.remove(settings.SPREADSHEETS_URL + fileName)
    return HttpResponse('{"Status" : "Success"}', content_type="application/json")


def getFileFromName(name):
    # your other codes ...
    file = open(settings.SPREADSHEETS_URL + name + ".xlsx", "rb").read()
    response = HttpResponse(file, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=' + name + '.xlsx';
    return response

def uploadFile(fileData , fileName):
    # your other codes ...
    file = open("RGG/spreadsheets/" + fileName + ".xlsx", "w")
    file.write(fileData)
    file.close()

    response = HttpResponse('{"Status" : "Success" , "FileData" : "'+fileData+'"}', content_type="application/json")
    return response

def getAllocationDecisionString(sheet_str):
    loc = settings.SPREADSHEETS_URL + sheet_str + ".xlsx"
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    allocation = get_allocation(sheet)
    rand = get_random_number()
    file = open(settings.NUMBER_MAPPING_URL)
    data = json.load(file)
    file.close()

    radial = data[sheet_str]["Radial"]
    rgg = data[sheet_str]["RGG"]

    radial = "+" + radial
    rgg = "+" + rgg

    if rand >= allocation:
        return radial
    else:
        return rgg

def getAllocationDecision(sheet_str):
    loc = settings.SPREADSHEETS_URL + sheet_str + ".xlsx"
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    allocation = get_allocation(sheet)
    rand = get_random_number()
    file = open(settings.NUMBER_MAPPING_URL)
    data = json.load(file)
    file.close()

    radial = data[sheet_str]["Radial"]
    rgg = data[sheet_str]["RGG"]

    radial = "+" + radial
    rgg = "+" + rgg

    if rand >= allocation:
        return HttpResponse(radial , content_type="text/plain")
    else:
        return HttpResponse(rgg , content_type="text/plain")

def getRelation(request):
    sheet_str = request.GET.get('sheet_name')
    loc = settings.SPREADSHEETS_URL + sheet_str + ".xlsx"
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    allocation = get_allocation(sheet)
    rand = get_random_number()
    file = open(settings.NUMBER_MAPPING_URL)
    data = json.load(file)
    file.close()

    radial = data[sheet_str]["Radial"]
    rgg = data[sheet_str]["RGG"]

    radial = "+" + radial
    rgg = "+" + rgg

    if rand >= allocation:
        return HttpResponse(radial , content_type="text/plain")
    else:
        return HttpResponse(rgg , content_type="text/plain")

def get_random_number():
    return random.randint(0,100)


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

def get_time_multiplier():
    multiplier = 1
    tz = timezone('US/Eastern')
    time_str = str(datetime.now(tz))

    time_arr = time_str.split(' ')
    time = time_arr[1].split(':')
    hours = time[0]
    minutes = time[1]

    hours = int(hours)
    multiplier = hours * 4 * multiplier
    minutes = int(minutes)
    if minutes < 30:
        minutes = "00"
    else:
        minutes = "30"
        multiplier += 2

    return multiplier

def get_correct_row(sheet , date):
    date_col = sheet.col_values(0)
    i = 0

    for i in range(len(date_col)):
        cell = sheet.cell_value(i , 0)
        if i == 0 or i == 1:
            continue
        cell_date = xlrd.xldate_as_tuple(cell, 0)
        year = cell_date[0]
        month = cell_date[1]
        day = cell_date[2]
        full_date_str = str(month) + "/" + str(day) + "/" + str(year)
        if date == full_date_str:
            return i

    return -1




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

def get_allocation(sheet):
    date = get_full_date()
    mult = get_time_multiplier()
    row = get_correct_row(sheet , date)
    if row == -1:
        return 100

    radial = sheet.cell_value(row , 1 + mult)
    rgg = sheet.cell_value(row , 2 + mult)
    if radial + rgg <= 0:
        return 0

    return (radial / (radial + rgg)) * 100





