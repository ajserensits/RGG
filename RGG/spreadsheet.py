"""
 Author: Andrew Serensits [ ajserensits@avaya.com ]

 This file is meant to handle all of the functionality that deals with reading
 spreadsheets of xlsx format and making a decision based off of that spreadsheet's
 content that dictates whether or not a call gets forwarded to Radial or RGG.

 This file also allows you to view the currently uploaded spreadsheets and/or delete
 them
"""

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

"""
 This function gives you all of the spreadsheet names in /media/spreadsheets/

 @param HttpRequest
 @return HttpResponse of type application/json containing all of the spreadsheets file names
"""
def getCurrentlyUploadedSpreadsheets(request):
    files = listdir(settings.SPREADSHEETS_URL)
    json_data = json.dumps(files)
    return HttpResponse(json_data, content_type="application/json")

"""
 This function allows you to delete a spreadsheet from /media/spreadsheets/

 @param HttpRequest with a GET parameter as the file_name to delete
 @return HttpResponse of type application/json indicating whether or not the file was successfully deleted
"""
def deleteSpreadsheet(request):
    fileName = request.GET.get('file_name')
    os.remove(settings.SPREADSHEETS_URL + fileName)
    return HttpResponse('{"Status" : "Success"}', content_type="application/json")

"""
 This function gives you a phone number from either Radial or RGG

 @param sheet_str of type string which is the Excel spreadsheet to look at
 @return string which represents the phone number to forward a call to
"""
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

"""
 This function gives you a phone number from either Radial or RGG

 @param sheet_str of type string which is the Excel spreadsheet to look at
 @return HttpResponse of type text/plain which represents the phone number to
         forward the call to
"""
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

"""
 This function gives you a phone number from either Radial or RGG

 @param request of type HttpRequest which contains a GET param as sheet_name
 @return HttpResponse of type text/plain which represents the phone number to
         forward the call to
"""
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

"""
 This function gives you a random number between 0 and 100 [inclusive]

 @param None
 @return Integer
"""
def get_random_number():
    return random.randint(0,100)

"""
 This function gives you the current time floored to the nearest half hour in the format that the spreadsheets
 expect which is HHMM in military time.

 IE: 9:30 PM becomes 2130

 Example function input ===> output
 If the current time is:
    1) 9:27 PM ===> 2100
    2) 9:31 PM ===> 2130
    3) 1:07 AM ===> 0100
    4) 12:38 PM ===> 1230

 @param None
 @return a string representing the time
"""
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

"""
 This function gives you the correct column index of the spreadsheet to look at.

 @param None
 @return an integer representing the index
"""
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


"""
 This function gives you the correct row index of the spreadsheet to look at.

 @param sheet of type xlrd spreadsheet  , date of type string expected format
                                          is MM/DD/YYYY
 @return an integer representing the index , -1 if it cannont be found
"""
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

"""
 This function gives you the date in MM/DD/YYYY format

 @param None
 @return a string in MM/DD/YYYY format
"""
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

"""
 This function goes through the allocation decision process and returns a number
 between 0 and 100.

 @param sheet of type xlrd spreadsheet
 @return a floating point number between 0 and 100
"""
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
