from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect as HRR, JsonResponse, HttpResponse, FileResponse
from .models import xss, commandinjection, sqlinjection, xxeinjection, nosqlinjection
from .forms import FormField
from .utils.get_request import get_request
from threading import Thread
from .utils.post_request import post_validation, post_request
from bs4 import BeautifulSoup as bs
import re
from requests.utils import requote_uri
import requests

# post method multiprocessing
# login DVWA and do post and get request there


results = []
threads = None


URL = "http://47.245.99.142/login.php"
host_up = True
context_data = {}

def hostDown(request):
    return render(request, "tools/host_down.html")

def get_view(url: str, type_attack: str):
    global results
    global host_up
    if (len(results) > 0):
        results.clear()
    try:
        if(type_attack == "xss"):
            result = get_request(url, list(xss.objects.values_list('payload', flat=True)))
        elif(type_attack == "sqli"):
            result = get_request(url, list(sqlinjection.objects.values_list('payload', flat=True)))
        elif(type_attack == "xxe"):
            result = get_request(url, list(xxeinjection.objects.values_list('payload', flat=True)))
        elif(type_attack == "command"):
            result = get_request(url, list(commandinjection.objects.values_list('payload', flat=True)))
        elif(type_attack == "nosql"):
            result = get_request(url, list(nosqlinjection.objects.values_list('payload', flat=True)))
    except Exception as e:
        print(e)
        host_up = False
        return
    results = result

def createSession(url):
    s = requests.Session()
    soup = bs(s.get(url).content, "html.parser")
    hidden = soup.find("input", type="hidden")
    token = hidden.get("value")
    payload = {"username": "admin", "password": "password", "Login":"Login", "user_token": token}
    s.post(url, data=payload)
    return s

def findInput(url):
    s = createSession(URL)
    content = s.get(url).content
    # content = requests.get(url).content
    soup = bs(content, "html.parser")
    input_form = soup.find_all("input")
    return [i.get("name") for i in input_form if i.get("name") is not None]

def postMethodValidation(url, type_attack):
    input_id = findInput(url)
    global context_data
    context_data = {
        "url": url,
        "input_id": input_id,
        "type_attack" : type_attack
    }

def post_view(url: str, type_attack: str):
    global results

    if(type_attack == "xss"):
        for p in xss.objects.all():
            pay = p.payload
            payload[key] = re.sub("\$[a-zA-Z0-9]*\$", pay, val)
            response = s.post(context_data['url'], data=payload[key])
            status_code = response.status_code
            try:
                content_length = response.headers["Content-Length"]
            except:
                content_length = len(response.text)
            results.append([pay, status_code, content_length])
            break
    elif(type_attack == "sqli"):
        result = get_request(url, list(sqlinjection.objects.values_list('payload', flat=True)))
    elif(type_attack == "xxe"):
        result = get_request(url, list(xxeinjection.objects.values_list('payload', flat=True)))
    elif(type_attack == "command"):
        result = get_request(url, list(commandinjection.objects.values_list('payload', flat=True)))
    elif(type_attack == "nosql"):
        result = get_request(url, list(nosqlinjection.objects.values_list('payload', flat=True)))
    
    results = result

def postMethodView(request):
    global results
    input_id = context_data["input_id"]
    type_attack = context_data["type_attack"]
    payload = {}
    if (len(results) > 0):
        results.clear()
    if request.method == 'POST':
        for key, value in request.POST.items():
            payload[key] = value
        for key, val in payload.items():
            if (type_attack == 'xss'):
                for p in xss.objects.all():
                    pay = p.payload
                    payload[key] = re.sub("\$[a-zA-Z0-9]*\$", pay, val)
                    # s = createSession(URL)
                    response = s.post(context_data['url'], data=payload[key])
                    status_code = response.status_code
                    try:
                        content_length = response.headers["Content-Length"]
                    except:
                        content_length = len(response.text)
                    results.append([pay, status_code, content_length])
                break
            elif (type_attack == 'sqli'):
                for p in sqlinjection.objects.all():
                    pay = p.payload
                    payload[key] = re.sub("\$[a-zA-Z0-9]*\$", pay, val)
                    # s = createSession(URL)

                    response = requests.post(context_data['url'], data=payload[key])
                    status_code = response.status_code
                    try:
                        content_length = response.headers["Content-Length"]
                    except:
                        content_length = len(response.text)
                    results.append([pay, status_code, content_length])
                break
            elif (type_attack == 'command'):
                for p in commandinjection.objects.all():
                    pay = p.payload
                    payload[key] = re.sub("\$[a-zA-Z0-9]*\$", pay, val)
                    # s = createSession(URL)
                    response = requests.post(context_data['url'], data=payload[key])
                    status_code = response.status_code
                    try:
                        content_length = response.headers["Content-Length"]
                    except:
                        content_length = len(response.text)
                    results.append([pay, status_code, content_length])
                break
            elif (type_attack == 'xxe'):
                for p in xxeinjection.objects.all():
                    pay = p.payload
                    payload[key] = re.sub("\$[a-zA-Z0-9]*\$", pay, val)
                    # s = createSession(URL)
                    response = s.post(context_data['url'], data=payload[key])
                    status_code = response.status_code
                    try:
                        content_length = response.headers["Content-Length"]
                    except:
                        content_length = len(response.text)
                    results.append([pay, status_code, content_length])
                break
            elif (type_attack == 'nosql'):
                for p in nosqlinjection.objects.all():
                    pay = p.payload
                    payload[key] = re.sub("\$[a-zA-Z0-9]*\$", pay, val)
                    # s = createSession(URL)
                    response = s.post(context_data['url'], data=payload[key])
                    status_code = response.status_code
                    try:
                        content_length = response.headers["Content-Length"]
                    except:
                        content_length = len(response.text)
                    results.append([pay, status_code, content_length])
                break
        return HRR("../result/") 
    return render(request, "tools/post_method.html", context_data)

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
        
        if (attack_method == "GET"):
            threads = Thread(target = get_view, args=(url, type_attack, ))
            threads.start()
            return redirect('check_thread_is_alive')
        
        elif (attack_method == "POST"): 
            postMethodValidation(url, type_attack)
            return HRR('method/post')

def createResult(request):
    return render(request, "tools/beta_tools.html", {"result": results})

def checkThreadIsAlive(request):
    return render(request, "tools/loading.html")

def loading_info(request):
    if (host_up == False):
        return HttpResponse("host is down")
    return HttpResponse(threads.is_alive())