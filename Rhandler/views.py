from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from Rhandler.models import UserInfo, Client, MessageFromDevice
import datetime

# Create your views here.


@csrf_exempt
# This method will send a message from phone to server
def SendMessageToClient(request):
    if 'logedin' not in request.session:
        jsonresponder = {"stat": "NOK", "Code": "2",
                         "DESC": "PLEAST LOGIN FIRST"}
        return JsonResponse(jsonresponder, JSONEncoder)
    else:
        if request.session['logedin'] == True:
            theUser = UserInfo.objects.get(pk=request.session['usid'])
            if request.POST['token'] == theUser.token:
                theClient = theUser.client_set.filter(
                    numberID=request.POST['client'])
                if theClient.count() == 1:
                    theClient = theUser.client_set.filter(
                        numberID=request.POST['client'])[0]
                else:
                    jsonresponder = {
                        "stat": "NOK", "Code": "3", "DESC": "Client is not Unique", "Number Of Clients": theClient.count()}
                    return JsonResponse(jsonresponder, JSONEncoder)
                msg = request.POST['message']
                val = request.POST['value']
                isr = False
                theTime = datetime.datetime.now()
                MessageFromDevice.objects.create(
                    message=msg, user=theUser, client=theClient, value=val, isRead=isr, time=theTime)
                jsonresponder = {"stat": "OK", "Code": "1",
                                 "DESC": "Message Has been SENT"}
                return JsonResponse(jsonresponder, JSONEncoder)
            else:
                jsonresponder = {"stat": "NOK", "Code": "4", , "DESC": "Token is Wrong"}
                return JsonResponse(jsonresponder, JSONEncoder)


@csrf_exempt
# This method will login a client to the serve , phone or ardino , both of them need login
def Login(request):
    if 'logedin' in request.session:
        jsonresponder = {"stat": "NOK", "Code": "5", , "DESC": "Already Loged In",
                         "Current User": request.session['user']}
        return JsonResponse(jsonresponder, JSONEncoder)
    if 'username' in request.POST:
        this_username = request.POST['username']
    else:
        jsonresponder = {"stat": "NOK", "Code": "6",
                         "DESC": "NO USERNAME FOUND"}
        return JsonResponse(jsonresponder, JSONEncoder)
    if 'password' in request.POST:
        this_password = request.POST['password']
    else:
        jsonresponder = {"stat": "NOK", "Code": "7",
                         "DESC": "NO PASSWORD FOUND"}
        return JsonResponse(jsonresponder, JSONEncoder)
    theUser = UserInfo.objects.filter(userName=this_username)
    if theUser.count():
        theUser = UserInfo.objects.get(userName=this_username)
        if theUser.password == this_password:
            request.session['logedin'] = True
            request.session['usid'] = theUser.id
            request.session['user'] = theUser.userName
            jsonresponder = {"stat": "OK", "Code": "1", "LOGEDIN": "TRUE"}
        else:
            request.session['logedin'] = False
            jsonresponder = {"stat": "OK",
                             "LOGEDIN": "FALSE", "Code": "8", "DESC": "Wrong Data"}
    else:
        request.session['logedin'] = False
        jsonresponder = {"stat": "OK",
                         "LOGEDIN": "FALSE", "Code": "8", "DESC": "Wrong Data"}

    return JsonResponse(jsonresponder, JSONEncoder)


@csrf_exempt
# This method will be launched from Arduino and check if any new message is avaiable or not .
def CheckNewMessageForClient(request):
    token = request.POST['token']
    theUser = UserInfo.objects.get(token=token)
    clientnumber = request.POST['client']
    client = Client.objects.get(numberID=clientnumber)
    message = MessageFromDevice.objects.filter(
        user=theUser, client=client, isRead=False).order_by('time')
    if not message.count():
        jsonresponder = {"stat": "OK", "counts": 0}
    else:
        jsonresponder = {"stat": "OK", "counts": 1,
                         "message": message[0].message, "val": message[0].value}
        up = MessageFromDevice.objects.get(pk=message[0].pk)
        up.isRead = True
        up.save()

    return JsonResponse(jsonresponder, JSONEncoder)
