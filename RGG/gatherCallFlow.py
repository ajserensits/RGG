"""
 Author: Andrew Serensits [ ajserensits@avaya.com ]

 This file is meant to handle all of the functionality that deals with the collecting digits portions of the call flows.
 It responds to any request with XML that corresponds to the documentation provided here [ https://docs.zang.io/aspx/inboundxml ]
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
from . import spreadsheet
from . import WorkflowConfig
from . import status
from . import logger
from . import settings


"""
 This function handles the menu selection / IVR portion of the call flows

 @param request is of type HttpRequest
 @return HttpResponse with a content_type of application/xml
"""
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
        if options[digits] == "spreadsheet": #Prepare to forward the call
            destination = spreadsheet.getAllocationDecisionString(actions[digits])
            forwardResponse = createForwardResponse(destination , _from)
            logger.updateForwardCallLog(sid , workflowName , destination)
            return HttpResponse(forwardResponse , content_type="application/xml")
        elif options[digits] == "dyk": #Play the did you know message
            dykResponse = createDYKResponse(dykMsg , workflowName , digits , sid , _from)
            logger.updateDYKCallLog(sid , workflowName)
            return HttpResponse(dykResponse , content_type="application/xml")
        else: #Error
            errorResponse = createErrorResponse
            return HttpResponse(errorResponse , content_type="application/xml")
    else:
        digits = default #Other
        destination = spreadsheet.getAllocationDecisionString(actions[digits])
        forwardResponse = createForwardResponse(destination , _from)
        logger.updateForwardCallLog(sid , workflowName , destination)
        return HttpResponse(forwardResponse , content_type="application/xml")



"""
 This function handles the menu selection / IVR portion of the call flows as it pertains to
 the 'Did you know?' portions.

 @param request is of type HttpRequest
 @return HttpResponse with a content_type of application/xml
"""
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

"""
 This function creates a response for the call that will provide the 'Did you know?' recording/mp3
 that is tied to this specific call flow.  This function returns an XML formatted string that contains the
 elements that play the DYK recording as well as gather element which allows us to collect digits

 @param dyk of type string (the recording/mp3 name) , workflowName of type string ,
        digits of type string (The digits pressed), sid of type string (Call SID) ,
        _from of type string (The person calling)
 @return a string in XML format.
"""
def createDYKResponse(dyk , workflowName , digits , sid , _from):
    playDYKElement = "<Play>" + settings.RECORDINGS_URL + dyk + ".mp3</Play>"
    gatherElement = "<Gather method = 'GET' numDigits='1' timeout='30' finishOnKey ='#' action = '" + settings.DYK_URL + "?workflow=" + workflowName + "&action=" + digits + "&sid=" + sid + "&from=" + _from + "'>" + playDYKElement + "</Gather>"
    xmlResponse = "<Response>" + gatherElement + "</Response>"
    return xmlResponse

"""
 This function creates a an error response for the call flow.

 @param None
 @return a string in XML format.
"""
def createErrorResponse():
    sayElement = "<Say> An error has occurred </Say>"
    xmlResponse = "<Response>" + sayElement + "</Response>"
    return xmlResponse

"""
 This function creates a response for the call that will forward the call to the proper destination.  This function returns an XML formatted string that contains the
 elements that will forward the call correctly.

 @param destination of type string (the number to forward the call to) , _from of type string (The calling party)
 @return a string in XML format.
"""
def createForwardResponse(destination , _from):
    dialElement = "<Dial callerId = '" + _from + "'>" + destination + "</Dial>"
    xmlResponse = "<Response>" + dialElement + "</Response>"
    return xmlResponse
