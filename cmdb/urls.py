from django.conf.urls import include, url

from cmdb.c_views import *
from common import views

urlpatterns = [
    url(r'^idc_level_list/idc_level_add_action', idc_level_add_action),
    url(r'^idc_level_list/idc_level_add', idc_level_add),
    url(r'^idc_level_list/delete_entity', idc_level_delete_entity),
    url(r'^idc_level_list/$', idc_level_list),
]
