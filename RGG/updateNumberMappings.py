"""
 Author: Andrew Serensits [ ajserensits@avaya.com ]

 This file is meant to handle all of the functionality that deals with updating
 and retrieving the number mappings for each call flow and each potential leg
 of each call flow.  These mappings dictate what number is a possibility of being
 forwarded to.
"""

import json
from django.http import HttpResponse
from . import auth
from . import settings

"""
 This function updates the number mappings for one call flow or one leg of the
 call flow

 @param HttpRequest
 @return HttpResponse of type application/json indicating a successful update
"""
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

"""
 This function gives you all of the number mappings in JSON

 @param HttpRequest
 @return HttpResponse of type application/json containing all of the number mappings 
"""
def getNumberMappings(request):
    json_data = open(settings.NUMBER_MAPPING_URL)
    data = json.load(json_data)
    response_data = json.dumps(data)

    return HttpResponse(response_data , content_type="application/json")
