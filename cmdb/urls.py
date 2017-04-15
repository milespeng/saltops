from django.conf.urls import include, url

from cmdb.c_views import *
from common import views

urlpatterns = [
    # 机房等级
    url(r'^idc_level_list/', include([
        url(r'(?P<pk>\d+)/idc_level_edit_action/', idc_level_edit_action),
        url(r'(?P<pk>\d+)/idc_level_edit/', idc_level_edit),
        url(r'idc_level_add_action/', idc_level_add_action),
        url(r'idc_level_add/', idc_level_add),
        url(r'(?P<pk>\d+)/delete_entity/', idc_level_delete_entity),
        url(r'$', idc_level_list, name='idc_level_list'),
    ])),

    # ISP
    url(r'^isp_list/', include([
        url(r'(?P<pk>\d+)/isp_edit_action/', isp_edit_action),
        url(r'(?P<pk>\d+)/isp_edit/', isp_edit),
        url(r'isp_add_action/', isp_add_action),
        url(r'isp_add/', isp_add),
        url(r'(?P<pk>\d+)/delete_entity/', isp_delete_entity),
        url(r'$', isp_list),
    ])),

    # IDC
    url(r'^idc_list/', include([
        url(r'idc_add/', idc_add),
        url(r'idc_add_action/', idc_add_action),
        url(r'(?P<pk>\d+)/elete_entity/', idc_delete_entity),
        url(r'(?P<pk>\d+)/idc_edit/', idc_edit),
        url(r'(?P<pk>\d+)/idc_edit_action/', idc_edit_action),
        url(r'$', idc_list),
    ])),

    # 机柜
    url(r'^cabinet_list/', include([
        url(r'cabinet_add/', cabinet_add),
        url(r'cabinet_add_action/', cabinet_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', cabinet_delete_entity),
        url(r'(?P<pk>\d+)/cabinet_edit/', cabinet_edit),
        url(r'(?P<pk>\d+)/cabinet_edit_action/', cabinet_edit_action),
        url(r'$', cabinet_list),
    ])),

    # 机架
    url('^rack_list/', include([
        url(r'rack_add/', rack_add),
        url(r'rack_add_action/', rack_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', rack_delete_entity),
        url(r'(?P<pk>\d+)/rack_edit/', rack_edit),
        url(r'(?P<pk>\d+)/rack_edit_action/', rack_edit_action),
        url(r'(?P<pk>\d+)/load_cabinet_list/', load_cabinet_list),
        url(r'(?P<idc_id>\d+)/(?P<cabinet_id>\d+)/load_rack_list/', load_rack_list),
        url(r'$', rack_list),
    ])),

    # 主机组
    url('^hostgroup_list/', include([
        url(r'hostgroup_add/', hostgroup_add),
        url(r'hostgroup_add_action/', hostgroup_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', hostgroup_delete_entity),
        url(r'(?P<pk>\d+)/hostgroup_edit/', hostgroup_edit),
        url(r'(?P<pk>\d+)/hostgroup_edit_action/', hostgroup_edit_action),
        url(r'$', hostgroup_list),
    ])),

    # 主机
    url('^host_list/', include([
        url(r'scan_host_job/', scan_host_job),
        url(r'host_add/', host_add),
        url(r'host_add_action/', host_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', host_delete_entity),
        url(r'(?P<pk>\d+)/host_edit/', host_edit),
        url(r'(?P<pk>\d+)/host_edit_action/', host_edit_action),
        url(r'$', host_list),
    ])),
]
