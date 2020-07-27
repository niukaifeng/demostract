"""demostract URL Configuration

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
from demostract.View import Index,UpdaLoad,LearningType,UpdaLoad2,Downloadfiel

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Index.as_view(),name='index'),

    path('uploadFile_1', UpdaLoad.as_view(),name='index'),

    path('uploadFile_2', UpdaLoad2.as_view(),name='index'),

    path('learningType', LearningType.as_view(),name='index'),

    path('downloadfiel', Downloadfiel.as_view(),name='downloadfiel'),







]
