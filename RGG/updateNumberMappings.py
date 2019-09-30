import json
from django.http import HttpResponse
from . import auth
from . import settings


def update(request):
    rgg = request.GET.get('rgg')
    radial = request.GET.get('radial')
    mapping = request.GET.get('mapping')

    user = request.GET.get('user')
    token = request.GET.get('token')

    if auth.isAuthenticatedBool(user , token) == False:
        return auth.isAuthenticated(user , token)

    file = open(settings.NUMBER_MAPPING_URL)
    data = json.load(file)
    file.close()

    data[mapping]["RGG"] = rgg
    data[mapping]["Radial"] = radial

    data = json.dumps(data)

    file = open(settings.NUMBER_MAPPING_URL, "w")
    file.write(data)
    file.close

    return HttpResponse('{"Status" : "Success"}' , content_type="application/json")

def getNumberMappings(request):
    json_data = open(settings.NUMBER_MAPPING_URL)
    data = json.load(json_data)
    response_data = json.dumps(data)

    return HttpResponse(response_data , content_type="application/json")