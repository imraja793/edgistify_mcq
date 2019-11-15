"""edgi_mcq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from mcq.views import UserProfileList, AddQuestionApi, Login, ApplicantResponse,\
    ApplicantMCQTestApi, GetQuestion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('UserProfileList/', UserProfileList.as_view()),
    path('AddQuestionApi/', AddQuestionApi.as_view()),
    path('Login/', Login.as_view()),
    path('ApplicantResponse/', ApplicantResponse.as_view()),
    path('ApplicantMCQTestApi/', ApplicantMCQTestApi.as_view()),
    path('GetQuestion/', GetQuestion.as_view()),

]
