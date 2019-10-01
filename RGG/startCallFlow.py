"""
 Author: Andrew Serensits [ ajserensits@avaya.com ]

 This file is meant to handle all of the functionality that deals with the initiation portion of the call flows.
 It responds to any request with XML that corresponds to the documentation provided here [ https://docs.zang.io/aspx/inboundxml ]
"""

import json
from django.http import HttpResponse
from . import spreadsheet
from . import WorkflowConfig
from . import status
from . import logger
from . import settings

"""
 This function handles the first leg of each call flow.  It decides whether
 to forward the call to a destination, to continue onto the next step of the
 call flow ( gatherCallFlow ) , or to drop the call because the call came outside
 of the hours of operation

 @param request is of type HttpRequest
 @return HttpResponse with a content_type of application/xml
"""
def start(request):
    workflow = request.GET.get('workflow')
    workflowName = workflow
    direction = request.GET.get('Direction')
    to = request.GET.get('To')
    _from = request.GET.get('From')
    sid = request.GET.get('CallSid')
    logger.updateStartCallLog(sid , _from , to , direction , workflowName)
    workflow = WorkflowConfig.getWorkflowByName(workflow)
    isItOpen = status.isItOpen()
    if isItOpen == "false":
        #TO-DO add if workflow is null
        closedMsg = workflow["Closed"]
        if workflowName.find('Gilt') == -1:
            closedResponse = createClosedResponse(closedMsg)
        else:
            closedResponse = createGiltClosedResponse()
        logger.updateClosedCallLog(sid , _from , to , direction , workflowName)
        return HttpResponse(closedResponse , content_type="application/xml")
    else:
        if workflow["Type"] == "Short":
            sheetName = workflow["Spreadsheet"]
            greetingMsg = workflow["Greeting"]
            destination = spreadsheet.getAllocationDecisionString(sheetName)
            shortResponse = createShortResponse(greetingMsg , destination , _from)
            logger.updateShortCallLog(sid , _from , to , direction , workflowName)
            return HttpResponse(shortResponse , content_type="application/xml")
        else:
            greetingMsg = workflow["Greeting"]
            menuMsg = workflow["Menu"]
            workflowName = workflow["Name"]
            mainResponse = createMainResponse(greetingMsg , menuMsg , workflowName , sid , _from)
            logger.updateMainCallLog(sid , _from , to , direction , workflowName)
            return HttpResponse(mainResponse , content_type="application/xml")


"""
 This function creates a response for the call that will provide the IVR Menu File (recording/mp3)
 that is tied to this specific call flow.  This function returns an XML formatted string that contains the
 elements that play the Menu recording as well as the <Gather> element which allows us to collect digits.
 The action url used for the <Gather> element links to the gatherCallFlow.py file

 This function is called on Workflows of type "Main"

 @param greeting of type string (the recording/mp3 name) ,
        menu of type string (the recording/mp3 name) ,
        workflowName of type string ,
        sid of type string (Call SID) ,
        _from of type string (The person calling)
 @return a string in XML format.
"""
def createMainResponse(greeting , menu , workflowName , call_sid , _from):
    recordingElement = "<Record background = 'true' timeout = '30' maxLength = '7200'/>"
    playGreetingElement = "<Play>" + settings.RECORDINGS_URL + greeting + ".mp3</Play>"
    playMenuElement = "<Play>" + settings.RECORDINGS_URL + menu + ".mp3</Play>"
    gatherElement = "<Gather method = 'GET' numDigits='1' timeout='30' finishOnKey ='#' action = '" + settings.GATHER_URL + "?workflow=" + workflowName + "&sid=" + call_sid + "&from=" + _from + "'>" + playMenuElement + "</Gather>"
    xmlResponse = "<Response>" + playGreetingElement + recordingElement + gatherElement + "</Response>"
    return xmlResponse

"""
 This function creates a response for the call that will provide the XML
 that forwards the call to its final destination.

 @param greeting of type string (the recording/mp3 name) ,
        destination of type string (who to forward to) ,
        _from of type string (The person calling)
 @return a string in XML format.
"""
def createShortResponse(greeting , destination , _from):
    recordingElement = "<Record background = 'true' timeout = '30' maxLength = '7200'/>"
    playGreetingElement = "<Play>" + settings.RECORDINGS_URL + greeting + ".mp3</Play>"
    dialElement = "<Dial callerId = '" + _from + "'>" + destination +"</Dial>"
    xmlResponse = "<Response>" + playGreetingElement + recordingElement + dialElement + "</Response>"
    return xmlResponse

"""
 This function creates a response for the call that will announce to the caller
 that the store is closed.

 @param closedMsgName of type string (the recording/mp3 name) ,
 @return a string in XML format.
"""
def createClosedResponse(closedMsgName):
    xmlResponse = "<Response><Play>" + settings.RECORDINGS_URL + closedMsgName + ".mp3</Play><Hangup/></Response>"
    return xmlResponse

def createGiltClosedResponse():
    msg = "Thank you for calling Gilt.  Our customer service center is currently closed.  We can be reached by phone 9AM to 9PM Eastern time, seven days a week.  You can also reach us at customer service at gilt dot com, or on our website at gilt dot com"
    xmlResponse = "<Response><Say voice = 'woman' language = 'en-us'>" + msg + "</Say><Hangup/></Response>"
    return xmlResponse
