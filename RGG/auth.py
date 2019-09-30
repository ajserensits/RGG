import json
import bcrypt
from datetime import datetime
from pytz import timezone
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import time
import string
import random
from . import settings



def logIn(request):
    username = request.GET.get('user')
    password = request.GET.get('password')
    verified = verifyUser(username , password)
    if verified["Verified"] == "True":
        token = createNewSession(username)
        return HttpResponse('{"Verified" : "True" , "User" : "' + username + '" , "Token" : "' + token + '"}' , content_type = "application/json")
    else:
        return HttpResponse('{"Verified" : "False" , "Reason" : "' + verified["Reason"] + '"}' , content_type="application/json")

def isAuthenticated(request):
    username = request.GET.get('user')
    token = request.GET.get('token')
    if isValidSession(username , token) == True:
        return HttpResponse('{"Authenticated" : "True"}' , content_type="application/json")
    else:
        return HttpResponse('{"Authenticated" : "False"}' , content_type="application/json")

def isAuthenticatedBool(username , token):
    if isValidSession(username , token) == True:
        return True
    else:
        return False



def getUser(name):
    json_data = open(settings.USER_CONFIG_URL)
    data = json.load(json_data)
    users = data["Users"]
    for i in range(len(users)):
        if users[i]["user"] == name:
            return users[i]

    return None

def verifyUser(username , password):
    response = {}
    if username == None or username == "":
        response["Verified"] = "False"
        response["Reason"] = "No User Matches "
        return response

    if password == None or password == "":
        response["Verified"] = "False"
        response["Reason"] = "No Password Provided "
        return response


    user = getUser(username)
    if user == None:
        response["Verified"] = "False"
        response["Reason"] = "No User Matches " + username
        return response

    if verify_password(user["password"] , password) == True:
        response["Verified"] = "True"
        return response
    else:
        response["Verified"] = "False"
        response["Reason"] = "Incorrect Password"
        return response

def isValidSession(username , token):
    if username == None or username == "":
        return False

    epoch_time = time.time()
    THREE_HOURS = 10800
    json_data = open(settings.SESSIONS_CONFIG_URL)
    data = json.load(json_data)
    sessions = data["Sessions"]
    for i in range(len(sessions)):
        if sessions[i]["user"] == username and sessions[i]["token"] == token and epoch_time - sessions[i]["start_time"] < THREE_HOURS:
            updateSession(username)
            return True

    return False

def createNewSession(username):
    epoch_time = time.time()
    json_data = open(settings.SESSIONS_CONFIG_URL)
    data = json.load(json_data)
    sessions = data["Sessions"]
    found = False
    for i in range(len(sessions)):
        if sessions[i]["user"] == username:
            sessions[i]["start_time"] = epoch_time
            auth_token = generateUniqueAuthToken()
            sessions[i]["token"] = auth_token
            found = True

    if found == False:
        new_session = {}
        new_session["user"] = username
        new_session["start_time"] = epoch_time
        auth_token = generateUniqueAuthToken()
        new_session["token"] = auth_token
        sessions.append(new_session)

    data["Sessions"] = sessions

    file_data = json.dumps(data)

    file = open(settings.SESSIONS_CONFIG_URL, "w")
    file.write(file_data)
    file.close()

    if auth_token is None:
        return "False"
    else:
        return auth_token

def updateSession(username):
    epoch_time = time.time()
    json_data = open(settings.SESSIONS_CONFIG_URL)
    data = json.load(json_data)
    sessions = data["Sessions"]
    for i in range(len(sessions)):
        if sessions[i]["user"] == username:
            sessions[i]["start_time"] = epoch_time
            found = True


    file_data = json.dumps(data)

    file = open(settings.SESSIONS_CONFIG_URL, "w")
    file.write(file_data)
    file.close()

def hash_password(password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(password, bcrypt.gensalt(12))

def verify_password(stored_password , provided_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(provided_password, stored_password)


def generateAuthToken():
    #string.punctuation
    #string.ascii_letters
    #string.digits
    #combinedList = string.punctuation + string.ascii_letters + string.digits
    combinedList = string.ascii_letters + string.digits

    token = ""
    i = 0
    while(i < 64):
        token = token + random.choice(combinedList)
        i += 1

    return token

def isUniqueToken(token):
    json_data = open(settings.SESSIONS_CONFIG_URL)
    data = json.load(json_data)
    sessions = data["Sessions"]
    for i in range(len(sessions)):
        if sessions[i]["token"] == token:
            return False

    return True

def generateUniqueAuthToken():
    token = generateAuthToken()
    while isUniqueToken(token) == False:
        token = generateAuthToken()

    return token



