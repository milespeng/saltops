from django.conf.urls import include, url

from cmdb.c_views import *
from common import views

urlpatterns = [
    # 机房等级
    url(r'^idc_level_list/(?P<pk>\d+)/idc_level_edit_action/', idc_level_edit_action),
    url(r'^idc_level_list/(?P<pk>\d+)/idc_level_edit/', idc_level_edit),
    url(r'^idc_level_list/idc_level_add_action/', idc_level_add_action),
    url(r'^idc_level_list/idc_level_add/', idc_level_add),
    url(r'^idc_level_list/delete_entity/', idc_level_delete_entity),
    url(r'^idc_level_list/$', idc_level_list),

    # ISP
    url(r'^isp_list/(?P<pk>\d+)/isp_edit_action/', isp_edit_action),
    url(r'^isp_list/(?P<pk>\d+)/isp_edit/', isp_edit),
    url(r'^isp_list/isp_add_action/', isp_add_action),
    url(r'^isp_list/isp_add/', isp_add),
    url(r'^isp_list/delete_entity/', isp_delete_entity),
    url(r'^isp_list/$', isp_list),

    # IDC
    url(r'^idc_list/$', idc_list),
    url(r'^idc_list/idc_add/', idc_add),
    url(r'^idc_list/idc_add_action/', idc_add_action),
    url(r'^idc_list/delete_entity/', idc_delete_entity),
    url(r'^idc_list/(?P<pk>\d+)/idc_edit/', idc_edit),
    url(r'^idc_list/(?P<pk>\d+)/idc_edit_action/', idc_edit_action),

    # 机柜
    url(r'^cabinet_list/$', cabinet_list),
    url(r'^cabinet_list/cabinet_add/', cabinet_add),
    url(r'^cabinet_list/cabinet_add_action/', cabinet_add_action),
    url(r'^cabinet_list/delete_entity/', cabinet_delete_entity),
    url(r'^cabinet_list/(?P<pk>\d+)/cabinet_edit/', cabinet_edit),
    url(r'^cabinet_list/(?P<pk>\d+)/cabinet_edit_action/', cabinet_edit_action),

    # 机架
    url(r'^rack_list/$', rack_list),
    url(r'^rack_list/rack_add/', rack_add),
    url(r'^rack_list/rack_add_action/', rack_add_action),
    url(r'^rack_list/delete_entity/', rack_delete_entity),
    url(r'^rack_list/(?P<pk>\d+)/rack_edit/', rack_edit),
    url(r'^rack_list/(?P<pk>\d+)/rack_edit_action/', rack_edit_action),
    url(r'^rack_list/(?P<pk>\d+)/load_cabinet_list/', load_cabinet_list),

]
