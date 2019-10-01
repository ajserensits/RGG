"""
 Author: Andrew Serensits [ ajserensits@avaya.com ]

 This file is meant to handle all of the functionality that deals with authorization and security.
 Things this file does:
   1) Allows the user to log in
   2) Checks to see if the user is logged in and authenticated
   3) Handles session creation and session validation
"""
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

"""
 This function handles the log on functionality.  It checks to see if the username and password provided are a match.

 @param request is of type HttpRequest
 @return HttpResponse with a content_type of json
"""
def logIn(request):
    username = request.GET.get('user')
    password = request.GET.get('password')
    verified = verifyUser(username , password)
    if verified["Verified"] == "True":
        token = createNewSession(username)
        return HttpResponse('{"Verified" : "True" , "User" : "' + username + '" , "Token" : "' + token + '"}' , content_type = "application/json")
    else:
        return HttpResponse('{"Verified" : "False" , "Reason" : "' + verified["Reason"] + '"}' , content_type="application/json")

"""
 This function checks if the request coming in is from an authorized user by looking at the user name and token provided

 @param request is of type HttpRequest
 @return HttpResponse with a content_type of json
"""
def isAuthenticated(request):
    username = request.GET.get('user')
    token = request.GET.get('token')
    if isValidSession(username , token) == True:
        return HttpResponse('{"Authenticated" : "True"}' , content_type="application/json")
    else:
        return HttpResponse('{"Authenticated" : "False"}' , content_type="application/json")

"""
 This function checks if the request coming in is from an authorized user by looking at the user name and token provided

 @param username is of type string, token is of type string
 @return Boolean
"""
def isAuthenticatedBool(username , token):
    if isValidSession(username , token) == True:
        return True
    else:
        return False

"""
 This function gets a user based off of the username provided

 @param name is of type string
 @return Dictionary if the user is found / None if not
"""
def getUser(name):
    json_data = open(settings.USER_CONFIG_URL)
    data = json.load(json_data)
    users = data["Users"]
    for i in range(len(users)):
        if users[i]["user"] == name:
            return users[i]

    return None

"""
 This function checks if the username and password provided match up with any records in the USER_CONFIG_URL file

 @param username of type string , password of type string
 @return Dictionary
"""
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

"""
 This function checks if username and token provided are part of a valid session

 @param username of type string , token of type string
 @return Boolean
"""
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

"""
 This function creates a new session for the username provided.  The length of the session is currently set to 3 hours.

 @param username of type string
 @return string: 'False' if unable to create the session , returns the auth token if successful
"""
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

"""
 This function updates a user's session by giving them 3 hours to be validated for.

 @param username of type string
 @return No return value
"""
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

"""
 This function hashes a password

 @param password of type string
 @return the hashed password of type string
"""
def hash_password(password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(password, bcrypt.gensalt(12))

"""
 This function checks the unhashed password against the hashed version

 @param stored_password of type string , provided_password of type string
 @return Boolean
"""
def verify_password(stored_password , provided_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(provided_password, stored_password)

"""
 This function generates a 64 character long auth token out of ascii letters and digits.

 @param None
 @return the token
"""
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

"""
 This function checks to see if the auth token provided is unique for the sessions

 @param token of type string
 @return Boolean
"""
def isUniqueToken(token):
    json_data = open(settings.SESSIONS_CONFIG_URL)
    data = json.load(json_data)
    sessions = data["Sessions"]
    for i in range(len(sessions)):
        if sessions[i]["token"] == token:
            return False

    return True

"""
 This function generates a 64 character long unique auth token out of ascii letters and digits.

 @param None
 @return token of type string
"""
def generateUniqueAuthToken():
    token = generateAuthToken()
    while isUniqueToken(token) == False:
        token = generateAuthToken()

    return token
