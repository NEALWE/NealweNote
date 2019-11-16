"""NoteBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
## vue整合添加，一行
from django.views.generic import TemplateView
from django.urls import path, include

##新增
from django.views import static
##新增
from django.conf import settings
##新增
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    ## vue整合添加，一行
    url(r'^$', TemplateView.as_view(template_name="index.html")),

    ##　以下是新增
    url(r'^note/upload/uploads/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    path('note/', include("Note.urls")),
    path('api/note/', include("Note.urls")),
]
