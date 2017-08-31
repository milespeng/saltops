# -*- coding: utf-8 -*-
"""saltops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework import routers

# from deploy_manager.serializer import UserViewSet
from common import views
from common.views import LoginView
from deploy_manager.views import *
from saltops import settings

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^app/', TemplateView.as_view(template_name="index.html")),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', LoginView.as_view(), name='index'),
    url(r'^checkLogin/$', views.checkLogin, name='checkLogin'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^mainform/$', views.mainform, name='mainform'),
    url(r'^dashboard/$', views.dashboard, name='mainform'),
    url(r'^frontend/cmdb/', include('cmdb.urls', namespace='cmdb')),
    url(r'^frontend/tools_manager/', include('tools_manager.urls', namespace='tools_manager')),
    url(r'^frontend/deploy_manager/', include('deploy_manager.urls', namespace='deploy_manager')),
    url(r'^frontend/base_auth/', include('base_auth.urls', namespace='base_auth')),
    url(r'^frontend/celery_manager/', include('celery_manager.urls', namespace='celery_manager'))
]
#
# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
admin.site.site_header = 'SaltOps'
admin.site.site_title = 'SaltOps'
