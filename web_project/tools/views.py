from django.shortcuts import render
from .forms import FormField
# Create your views here.
def index(request):
    form_field = FormField()
    
    context = {
        'data_form':form_field
    }
    print(request.POST)
    return render(request, 'tools/index.html',context)