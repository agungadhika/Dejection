from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect as HRR
from .models import xss, commandinjection, sqlinjection, xxeinjection, nosqlinjection

from .forms import FormField
from .utils.get_request import get_request

def get_view(url, type_attack):
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
    
    return result

def index(request):
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
            result = get_view(url, type_attack)
        # elif (attack_method == "POST"): 
        #     result = post_view(type_attack)