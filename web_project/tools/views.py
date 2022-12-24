from django.shortcuts import render
from .models import xss
from .forms import FormField
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
def index(request):
    if request.method == "POST":
        form_field = FormField(request.POST)
        if (form_field.is_valid()):
            url = form_field.cleaned_data["url_field"]
            # print(re.sub("\$[a-zA-Z0-9]*\$", url))
            type_attack = form_field.cleaned_data['type_attack']
            print(type(type_attack))
            if(type_attack == 'xss'):
                print(xss.objects.values_list("payload"))
                get_object = xss.objects.values("payload").get(id=1)['payload']
                submit = re.sub("\$[a-zA-Z0-9]*\$", get_object, url)
                print(submit)
            os.system(f'curl -X POST "{submit}"')
            print(url, type_attack)
    else:
        form_field = FormField()
    context = {
        'data_form':form_field
    }
    return render(request, 'tools/index.html', context)