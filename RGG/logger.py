import json
from datetime import datetime
from pytz import timezone
from django.http import HttpResponse
import os
from os import listdir
from os.path import isfile, join
from . import settings


def updateStartCallLog(sid , _from , to , direction , workflow):
    try:
        tz = timezone('US/Eastern')
        time_str = str(datetime.now(tz))

        entry_begin = "-------------------------------------------------------\n"
        entry_middle = "Call SID: " + sid + "\nFrom: " + _from + "\nTo: " + to + "\nDirection: " + direction + "\nWorkflow: " + workflow
        entry_end = "\n-------------------------------------------------------\n"

        entry = entry_begin + entry_middle + entry_end

        file = open(settings.START_LOG_URL, "a+")
        file.write(entry)
        file.close()
    except:
        return

def updateClosedCallLog(sid , _from , to , direction , workflow):
    try:
        tz = timezone('US/Eastern')
        time_str = str(datetime.now(tz))

        entry_begin = "-------------------------------------------------------\n"
        entry_middle = "Call SID: " + sid + "\nFrom: " + _from + "\nTo: " + to + "\nDirection: " + direction + "\nWorkflow: " + workflow
        entry_end = "\n-------------------------------------------------------\n"

        entry = entry_begin + entry_middle + entry_end

        file = open(settings.CLOSED_LOG_URL, "a+")
        file.write(entry)
        file.close()
    except:
        return

def updateShortCallLog(sid , _from , to , direction , workflow):
    try:
        tz = timezone('US/Eastern')
        time_str = str(datetime.now(tz))

        entry_begin = "-------------------------------------------------------\n"
        entry_middle = "Call SID: " + sid + "\nFrom: " + _from + "\nTo: " + to + "\nDirection: " + direction + "\nWorkflow: " + workflow
        entry_end = "\n-------------------------------------------------------\n"

        entry = entry_begin + entry_middle + entry_end

        file = open(settings.SHORT_LOG_URL, "a+")
        file.write(entry)
        file.close()
    except:
        return

def updateMainCallLog(sid , _from , to , direction , workflow):
    try:
        tz = timezone('US/Eastern')
        time_str = str(datetime.now(tz))

        entry_begin = "-------------------------------------------------------\n"
        entry_middle = "Call SID: " + sid + "\nFrom: " + _from + "\nTo: " + to + "\nDirection: " + direction + "\nWorkflow: " + workflow
        entry_end = "\n-------------------------------------------------------\n"

        entry = entry_begin + entry_middle + entry_end

        file = open(settings.MAIN_LOG_URL, "a+")
        file.write(entry)
        file.close()
    except:
        return

def updateForwardCallLog(sid , workflow , destination):
    try:
        tz = timezone('US/Eastern')
        time_str = str(datetime.now(tz))

        entry_begin = "-------------------------------------------------------\n"
        entry_middle = "Call SID: " + sid + "\nWorkflow: " + workflow + "\nDestination: " + destination
        entry_end = "\n-------------------------------------------------------\n"

        entry = entry_begin + entry_middle + entry_end

        file = open(settings.FORWARD_LOG_URL, "a+")
        file.write(entry)
        file.close()
    except:
        return

def updateDYKCallLog(sid , workflow):
    try:
        tz = timezone('US/Eastern')
        time_str = str(datetime.now(tz))

        entry_begin = "-------------------------------------------------------\n"
        entry_middle = "Call SID: " + sid + "\nWorkflow: " + workflow
        entry_end = "\n-------------------------------------------------------\n"

        entry = entry_begin + entry_middle + entry_end

        file = open(settings.DYK_LOG_URL, "a+")
        file.write(entry)
        file.close()
    except:
        return

