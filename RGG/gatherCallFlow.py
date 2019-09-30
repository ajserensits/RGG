import xlrd
import random
import json
from datetime import datetime
from pytz import timezone
from django.http import HttpResponse
import os
from os import listdir
from os.path import isfile, join
from . import spreadsheet
from . import WorkflowConfig
from . import status
from . import logger
from . import settings



def main(request):
    workflow = request.GET.get('workflow')
    sid = request.GET.get('sid')
    _from = request.GET.get('from')
    digits = request.GET.get('Digits')
    workflow = WorkflowConfig.getWorkflowByName(workflow)
    dykMsg = workflow["DYK"]
    workflowName = workflow["Name"]
    options = workflow["Options"]
    actions = workflow["Actions"]
    dykRepeat = workflow["DYK_Repeat"]
    default = workflow["Default"]
    if digits in options:
        if options[digits] == "spreadsheet":
            destination = spreadsheet.getAllocationDecisionString(actions[digits])
            forwardResponse = createForwardResponse(destination , _from)
            logger.updateForwardCallLog(sid , workflowName , destination)
            return HttpResponse(forwardResponse , content_type="application/xml")
        elif options[digits] == "dyk":
            dykResponse = createDYKResponse(dykMsg , workflowName , digits , sid , _from)
            logger.updateDYKCallLog(sid , workflowName)
            return HttpResponse(dykResponse , content_type="application/xml")
        else:
            errorResponse = createErrorResponse
            return HttpResponse(errorResponse , content_type="application/xml")
    else:
        digits = default #Other
        destination = spreadsheet.getAllocationDecisionString(actions[digits])
        forwardResponse = createForwardResponse(destination , _from)
        logger.updateForwardCallLog(sid , workflowName , destination)
        return HttpResponse(forwardResponse , content_type="application/xml")




def dyk(request):
    workflow = request.GET.get('workflow')
    digits = request.GET.get('Digits')
    sid = request.GET.get('sid')
    action = request.GET.get('action')
    _from = request.GET.get('from')
    workflow = WorkflowConfig.getWorkflowByName(workflow)
    dykMsg = workflow["DYK"]
    workflowName = workflow["Name"]
    options = workflow["Options"]
    actions = workflow["Actions"]
    dykRepeat = workflow["DYK_Repeat"]
    if digits == dykRepeat["Continue"]:
        destination = spreadsheet.getAllocationDecisionString(actions[action])
        forwardResponse = createForwardResponse(destination , _from)
        logger.updateForwardCallLog(sid , workflowName , destination)
        return HttpResponse(forwardResponse , content_type="application/xml")
    else:
        dykResponse = createDYKResponse(dykMsg , workflowName , digits , sid , _from)
        logger.updateDYKCallLog(sid , workflowName)
        return HttpResponse(dykResponse , content_type="application/xml")

def createDYKResponse(dyk , workflowName , digits , sid , _from):
    playDYKElement = "<Play>" + settings.RECORDINGS_URL + dyk + ".mp3</Play>"
    gatherElement = "<Gather method = 'GET' numDigits='1' timeout='30' finishOnKey ='#' action = '" + settings.DYK_URL + "?workflow=" + workflowName + "&action=" + digits + "&sid=" + sid + "&from=" + _from + "'>" + playDYKElement + "</Gather>"
    xmlResponse = "<Response>" + gatherElement + "</Response>"
    return xmlResponse

def createErrorResponse():
    sayElement = "<Say> An error has occurred </Say>"
    xmlResponse = "<Response>" + sayElement + "</Response>"
    return xmlResponse

def createForwardResponse(destination , _from):
    dialElement = "<Dial callerId = '" + _from + "'>" + destination + "</Dial>"
    xmlResponse = "<Response>" + dialElement + "</Response>"
    return xmlResponse










