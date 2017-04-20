from django.conf.urls import include, url

from cmdb.c_views import *
from common import views
from common.common_views import *

urlpatterns = [
    # 机房等级
    url(r'^idc_level_list/', include([
        url(r'(?P<pk>\d+)/idc_level_edit_action/', simple_edit_action),
        url(r'(?P<pk>\d+)/idc_level_edit/', simple_edit),
        url(r'idc_level_add_action/', simple_add_action),
        url(r'idc_level_add/', simple_add),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'modulename': 'cmdb.models',
            'modelname': 'IDCLevel',
            'list_url': '/frontend/cmdb/idc_level_list/',
            'form_template_path': 'frontend/common/basic_form.html',
            'template_path': 'frontend/cmdb/idc_level_list.html',
            'add_fields': '__all__',
            'add_title': '新增机房等级',
            'add_action': '/frontend/cmdb/idc_level_list/idc_level_add_action/',
            'edit_fields': '__all__',
            'edit_title': '编辑机房等级',
            'edit_action': '/frontend/cmdb/idc_level_list/%s/idc_level_edit_action/',
        }),

    # ISP
    url(r'^isp_list/', include([
        url(r'(?P<pk>\d+)/isp_edit_action/', simple_edit_action),
        url(r'(?P<pk>\d+)/isp_edit/', simple_edit),
        url(r'isp_add_action/', simple_add_action),
        url(r'isp_add/', simple_add),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'modulename': 'cmdb.models',
            'modelname': 'ISP',
            'list_url': '/frontend/cmdb/isp_list/',
            'form_template_path': 'frontend/common/basic_form.html',
            'template_path': 'frontend/cmdb/isp_list.html',
            'add_fields': '__all__',
            'add_title': '新增ISP',
            'add_action': '/frontend/cmdb/isp_list/isp_add_action/',
            'edit_fields': '__all__',
            'edit_title': '编辑ISP',
            'edit_action': '/frontend/cmdb/isp_list/%s/isp_edit_action/',
        }),

    # IDC
    url(r'^idc_list/', include([
        url(r'idc_add/', simple_add),
        url(r'idc_add_action/', simple_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'(?P<pk>\d+)/idc_edit/', simple_edit),
        url(r'(?P<pk>\d+)/idc_edit_action/', simple_edit_action),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'modulename': 'cmdb.models',
            'modelname': 'IDC',
            'list_url': '/frontend/cmdb/idc_list/',
            'form_template_path': 'frontend/common/basic_form.html',
            'template_path': 'frontend/cmdb/idc_list.html',
            'add_fields': '__all__',
            'add_title': '新增机房',
            'add_action': '/frontend/cmdb/idc_list/idc_add_action/',
            'edit_fields': '__all__',
            'edit_title': '编辑机房',
            'edit_action': '/frontend/cmdb/idc_list/%s/idc_edit_action/',
            'plugin_name': 'idc_list_plugin'
        }),

    # 机柜
    url(r'^cabinet_list/', include([
        url(r'cabinet_add/', simple_add),
        url(r'cabinet_add_action/', simple_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'(?P<pk>\d+)/cabinet_edit/', simple_edit),
        url(r'(?P<pk>\d+)/cabinet_edit_action/', simple_edit_action),
        url(r'$', simple_list),
    ]), {
            'modulename': 'cmdb.models',
            'modelname': 'Cabinet',
            'list_url': '/frontend/cmdb/cabinet_list/',
            'form_template_path': 'frontend/common/basic_form.html',
            'template_path': 'frontend/cmdb/cabinet_list.html',
            'add_fields': '__all__',
            'add_title': '新增机柜',
            'add_action': '/frontend/cmdb/cabinet_list/cabinet_add_action/',
            'edit_fields': '__all__',
            'edit_title': '编辑机柜',
            'edit_action': '/frontend/cmdb/cabinet_list/%s/cabinet_edit_action/',
            'plugin_name': 'idc_list_plugin'
        }),

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
