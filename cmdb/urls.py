from django.conf.urls import include, url

from cmdb.c_views import idc_level_list
from common import views

urlpatterns = [
    url(r'^idc_level_list/$', idc_level_list),
]
