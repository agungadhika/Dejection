"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from documentation import views as documentations
from cvss import views as cv
from tools import views as tools

urlpatterns = [
    path('', views.index),
    path('tools/', tools.index),
    path('documentation/', documentations.index),
    path('admin/', admin.site.urls),
    path('cvss/', cv.index),
    path('tools/result/', tools.createResult, name="result"),
    path('tools/loading_info', tools.loading_info, name="loading_info"),
    path('tools/loading', tools.checkThreadIsAlive, name="check_thread_is_alive"),
    path('tools/method/post/validation', tools.postMethodValidation, name="post_validation"),
    # path('tools/method/post', tools.postMethodView, name="post_process"),
    path('tools/host_down', tools.hostDown, name="host_down")
    # path('beta_tools/', tools.beta_tools, name='beta_tools'),
    # path('beta_tools/download_pdf/', tools.download_pdf, name='download_pdf'),
]
