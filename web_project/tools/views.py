from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect as HRR, JsonResponse, HttpResponse, FileResponse
from .models import xss, commandinjection, sqlinjection, xxeinjection, nosqlinjection
from .forms import FormField
from .utils.get_request import get_request
from threading import Thread
# from .utils.post_request import post_validation, post_request
from bs4 import BeautifulSoup as bs
import re
from requests.utils import requote_uri
import requests
from .utils.post_request import post_validation, post_request, URL, post_request_nosql

# post method multiprocessing
# login DVWA and do post and get request there

results = []
threads = None
login_dvwa = True # change to true when checking Bwapp

URL = URL
host_up = True
context_data = {}

def hostDown(request):
    return render(request, "tools/host_down.html")

def get_view(url: str, type_attack: str):
    global results
    global host_up
    # login_dvwa = True
    if (len(results) > 0):
        results.clear()
    try:
        if(type_attack == "xss"):
            result = get_request(url, list(xss.objects.values_list('payload', flat=True)), login_dvwa = login_dvwa)
        elif(type_attack == "sqli"):
            result = get_request(url, list(sqlinjection.objects.values_list('payload', flat=True)), login_dvwa = login_dvwa)
        elif(type_attack == "xxe"):
            result = get_request(url, list(xxeinjection.objects.values_list('payload', flat=True)), login_dvwa = login_dvwa)
        elif(type_attack == "command"):
            result = get_request(url, list(commandinjection.objects.values_list('payload', flat=True)), login_dvwa = login_dvwa)
        elif(type_attack == "nosql"):
            result = get_request(url, list(nosqlinjection.objects.values_list('payload', flat=True)), login_dvwa = login_dvwa)
    except Exception as e:
        print(e)
        host_up = False
        return
    results = result

def postMethodValidation(request):
    global threads
    url = request.session["url"]
    type_attack = request.session["type_attack"]
    context_data = post_validation(url, type_attack, login_dvwa = login_dvwa)
    
    if (request.method == "GET"):
        if(type_attack == "nosql"):
            return render(request, "tools/nosql_post_method.html")
        return render(request, "tools/post_method.html", context=context_data)
    else:
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken", None) # removing the csrfmiddlewaretokens
        
        threads = Thread(target = postMethodView, args=(url, type_attack, data))
        threads.start()
        # print(xss.objects.values_list("payload", flat=True))
        return redirect('check_thread_is_alive')

def deleteEmptyString(payload_list):
    result = [r for r in payload_list if r != ""]
    return result

def postMethodView(url, type_attack, data):
    global results
    # login_dvwa = False

    if(len(results) > 0):
        results.clear()
    
    if(type_attack == "xss"):
        result = post_request(url, deleteEmptyString(list(xss.objects.values_list('payload', flat=True))), data, login_dvwa = login_dvwa)
    elif(type_attack == "sqli"):
        result = post_request(url, deleteEmptyString(list(sqlinjection.objects.values_list('payload', flat=True))), data, login_dvwa = login_dvwa)
    elif(type_attack == "xxe"):
        result = post_request(url, deleteEmptyString(list(xxeinjection.objects.values_list('payload', flat=True))), data, login_dvwa = login_dvwa)
    elif(type_attack == "command"):
        result = post_request(url, deleteEmptyString(list(commandinjection.objects.values_list('payload', flat=True))), data, login_dvwa = login_dvwa)
    elif(type_attack == "nosql"):
        result = post_request_nosql(url=url, data=data, payloads=list(nosqlinjection.objects.values_list('payload', flat=True)), login_dvwa=login_dvwa, json_encode = True)
    
    results = result

def index(request):
    global threads
    if request.method == "GET":
        context = {
            'data_form': FormField()
        }
        return render(request, "tools/index.html", context)
    if request.method == "POST":
        form_field = FormField(request.POST)
        if (form_field.is_valid()):
            url = form_field.cleaned_data["url_field"]
            type_attack = form_field.cleaned_data['type_attack']
            attack_method = form_field.cleaned_data['attack_method']
            request.session["url"] = url
            request.session["type_attack"] = type_attack

        if (attack_method == "GET"):
            threads = Thread(target = get_view, args=(url, type_attack, ))
            threads.start()
            return redirect('check_thread_is_alive')
        
        elif (attack_method == "POST"): 
            return redirect('post_validation')

def createResult(request):
    return render(request, "tools/beta_tools.html", {"result": results})

def checkThreadIsAlive(request):
    return render(request, "tools/loading.html")

def loading_info(request):
    if (host_up == False):
        return HttpResponse("host is down")
    return HttpResponse(threads.is_alive())


"""
no sql
kita perlu satu input yang blank,
input menerima string, tanpa encode langsung dikirim.

Saat post validation, buat sebuah checkmark yang menandakan apakah 
input/select list akan dibypass atau tidak.


"""