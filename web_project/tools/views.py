from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect as HRR
from .models import xss
from .forms import FormField
import requests
import os
import re

# Create your views here.
# def index(request):
#     form_field = FormField()
    
#     context = {
#         'data_form':form_field
#     }
#     print(request.POST)
#     return render(request, 'tools/index.html',context)
response_code = ""
content_length = ""
payload = ""

def index(request):
    global response_code
    global content_length
    global payload
    if request.method == "POST":
        form_field = FormField(request.POST)
        if (form_field.is_valid()):
            url = form_field.cleaned_data["url_field"]
            # print(re.sub("\$[a-zA-Z0-9]*\$", url))
            type_attack = form_field.cleaned_data['type_attack']
            # print(type(type_attack))
            if(type_attack == 'xss'):
                # print(xss.objects.values_list("payload"))
                payload = xss.objects.values("payload").get(id=1)['payload']
                submit = re.sub("\$[a-zA-Z0-9]*\$", payload, url)
                # print(submit)
            # result = os.system(f'curl -X POST "{submit}"')
            # result = requests.post(submit, json={"username":"hello", "password":"world"})
            response = requests.post(submit) 
            response_code  = response.status_code
            content_length = len(response.content)
            return HRR("result/")
    else:
        form_field = FormField()
    context = {
        'data_form':form_field
    }
    return render(request, 'tools/index.html', context)

def createResult(request):
    return render(request, "tools/tools.html", {"response_code": response_code, "content_length": content_length, "payload": payload})