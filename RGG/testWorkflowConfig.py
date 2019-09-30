import json
from django.http import HttpResponse
from . import settings



def update(request):
    rgg = request.GET.get('rgg')
    radial = request.GET.get('radial')
    mapping = request.GET.get('mapping')

    file = open(settings.WORKFLOW_CONFIG_URL)
    data = json.load(file)
    file.close()

    data[mapping]["RGG"] = rgg
    data[mapping]["Radial"] = radial

    data = json.dumps(data)

    #file = open(WORKFLOW_CONFIG_URL, "w")
    file.write(data)
    file.close

    return HttpResponse('{"Status" : "Success"}' , content_type="application/json")

def getNumberMappings(request):
    json_data = open(settings.WORKFLOW_CONFIG_URL)
    data = json.load(json_data)
    response_data = json.dumps(data)

    return HttpResponse(response_data , content_type="application/json")

def getWorkflowByName(name):
    json_data = open(settings.WORKFLOW_CONFIG_URL)
    data = json.load(json_data)
    workflows = data["Workflows"]
    for i in range(len(workflows)):
        if workflows[i]["Name"] == name:
            return workflows[i]

    return None


def test():
    json_data = open(settings.WORKFLOW_CONFIG_URL)
    data = json.load(json_data)
    workflows = data["Workflows"]
    for i in range(len(workflows)):
        if workflows[i]["Type"] == "Main":
            print(workflows[i])


workflow = getWorkflowByName("Gilt_Noir_Main")
print(workflow)
