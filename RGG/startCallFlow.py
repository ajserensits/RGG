import json
from django.http import HttpResponse
from . import spreadsheet
from . import WorkflowConfig
from . import status
from . import logger
from . import settings

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



def createMainResponse(greeting , menu , workflowName , call_sid , _from):
    recordingElement = "<Record background = 'true' timeout = '30' maxLength = '7200'/>"
    playGreetingElement = "<Play>" + settings.RECORDINGS_URL + greeting + ".mp3</Play>"
    playMenuElement = "<Play>" + settings.RECORDINGS_URL + menu + ".mp3</Play>"
    gatherElement = "<Gather method = 'GET' numDigits='1' timeout='30' finishOnKey ='#' action = '" + settings.GATHER_URL + "?workflow=" + workflowName + "&sid=" + call_sid + "&from=" + _from + "'>" + playMenuElement + "</Gather>"
    xmlResponse = "<Response>" + playGreetingElement + recordingElement + gatherElement + "</Response>"
    return xmlResponse


def createShortResponse(greeting , destination , _from):
    recordingElement = "<Record background = 'true' timeout = '30' maxLength = '7200'/>"
    playGreetingElement = "<Play>" + settings.RECORDINGS_URL + greeting + ".mp3</Play>"
    dialElement = "<Dial callerId = '" + _from + "'>" + destination +"</Dial>"
    xmlResponse = "<Response>" + playGreetingElement + recordingElement + dialElement + "</Response>"
    return xmlResponse


def createClosedResponse(closedMsgName):
    xmlResponse = "<Response><Play>" + settings.RECORDINGS_URL + closedMsgName + ".mp3</Play><Hangup/></Response>"
    return xmlResponse

def createGiltClosedResponse():
    msg = "Thank you for calling Gilt.  Our customer service center is currently closed.  We can be reached by phone 9AM to 9PM Eastern time, seven days a week.  You can also reach us at customer service at gilt dot com, or on our website at gilt dot com"
    xmlResponse = "<Response><Say voice = 'woman' language = 'en-us'>" + msg + "</Say><Hangup/></Response>"
    return xmlResponse








