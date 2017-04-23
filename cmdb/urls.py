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
            'args': {
                'modulename': 'cmdb.models',
                'modelname': 'IDCLevel',
                'list_url': '/frontend/cmdb/idc_level_list/',
                'form_template_path': 'frontend/common/basic_form.html',
                'template_path': 'frontend/cmdb/idc_level_list.html',
                'add_title': '新增机房等级',
                'add_action': '/frontend/cmdb/idc_level_list/idc_level_add_action/',
                'edit_title': '编辑机房等级',
                'edit_action': '/frontend/cmdb/idc_level_list/%s/idc_level_edit_action/',
            }
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
            'args': {
                'modulename': 'cmdb.models',
                'modelname': 'ISP',
                'list_url': '/frontend/cmdb/isp_list/',
                'form_template_path': 'frontend/common/basic_form.html',
                'template_path': 'frontend/cmdb/isp_list.html',
                'add_title': '新增ISP',
                'add_action': '/frontend/cmdb/isp_list/isp_add_action/',
                'edit_title': '编辑ISP',
                'edit_action': '/frontend/cmdb/isp_list/%s/isp_edit_action/',
            }}),

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
            'args': {
                'modulename': 'cmdb.models',
                'modelname': 'IDC',
                'list_url': '/frontend/cmdb/idc_list/',
                'form_template_path': 'frontend/common/basic_form.html',
                'template_path': 'frontend/cmdb/idc_list.html',
                'add_title': '新增机房',
                'add_action': '/frontend/cmdb/idc_list/idc_add_action/',
                'edit_title': '编辑机房',
                'edit_action': '/frontend/cmdb/idc_list/%s/idc_edit_action/',
                'plugin_name': 'idc_list_plugin'
            }}),

    # 机柜
    url(r'^cabinet_list/', include([
        url(r'cabinet_add/', simple_add),
        url(r'cabinet_add_action/', simple_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'(?P<pk>\d+)/cabinet_edit/', simple_edit),
        url(r'(?P<pk>\d+)/cabinet_edit_action/', simple_edit_action),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'args': {
                'modulename': 'cmdb.models',
                'modelname': 'Cabinet',
                'list_url': '/frontend/cmdb/cabinet_list/',
                'form_template_path': 'frontend/common/basic_form.html',
                'template_path': 'frontend/cmdb/cabinet_list.html',
                'add_title': '新增机柜',
                'add_action': '/frontend/cmdb/cabinet_list/cabinet_add_action/',
                'edit_title': '编辑机柜',
                'edit_action': '/frontend/cmdb/cabinet_list/%s/cabinet_edit_action/',
                'plugin_name': 'idc_list_plugin'
            }}),

    url(r'^rack_list/(?P<idc_id>\d+)/(?P<cabinet_id>\d+)/load_rack_list/', load_rack_list),
    url(r'^rack_list/(?P<pk>\d+)/load_cabinet_list/', load_cabinet_list),
    # 机架
    url('^rack_list/', include([
        url(r'rack_add/', simple_add),
        url(r'rack_add_action/', simple_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'(?P<pk>\d+)/rack_edit/', simple_edit),
        url(r'(?P<pk>\d+)/rack_edit_action/', simple_edit_action),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'args': {
                'modulename': 'cmdb.models',
                'modelname': 'Rack',
                'list_url': '/frontend/cmdb/rack_list/',
                'form_template_path': 'frontend/cmdb/rack_form.html',
                'template_path': 'frontend/cmdb/rack_list.html',
                'add_title': '新增机架',
                'add_action': '/frontend/cmdb/rack_list/rack_add_action/',
                'edit_title': '编辑机架',
                'edit_action': '/frontend/cmdb/rack_list/%s/rack_edit_action/',
                'plugin_name': 'idc_list_plugin',
                'edit_form_plugin': 'rack_edit_form_plugin',
                'add_form_plugin': 'rack_add_form_plugin'
            }}),

    # 主机组
    url('^hostgroup_list/', include([
        url(r'hostgroup_add/', simple_add),
        url(r'hostgroup_add_action/', simple_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'(?P<pk>\d+)/hostgroup_edit/', simple_edit),
        url(r'(?P<pk>\d+)/hostgroup_edit_action/', simple_edit_action),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'args': {
                'modulename': 'cmdb.models',
                'modelname': 'HostGroup',
                'list_url': '/frontend/cmdb/hostgroup_list/',
                'form_template_path': 'frontend/common/basic_form.html',
                'template_path': 'frontend/cmdb/hostgroup_list.html',
                'add_title': '新增主机组',
                'add_action': '/frontend/cmdb/hostgroup_list/hostgroup_add_action/',
                'edit_title': '编辑主机组',
                'edit_action': '/frontend/cmdb/hostgroup_list/%s/hostgroup_edit_action/',
            }}),

    url(r'host_list/scan_host_job/', scan_host_job),
    # 主机
    url('^host_list/', include([
        url(r'host_add/', simple_add),
        url(r'host_add_action/', simple_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'(?P<pk>\d+)/host_edit/', simple_edit),
        url(r'(?P<pk>\d+)/host_edit_action/', simple_edit_action),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'args': {
                'modulename': 'cmdb.models',
                'modelname': 'Host',
                'list_url': '/frontend/cmdb/host_list/',
                'form_template_path': 'frontend/cmdb/host_form.html',
                'template_path': 'frontend/cmdb/host_list.html',
                'add_title': '新增主机',
                'add_action': '/frontend/cmdb/host_list/host_add_action/',
                'edit_title': '编辑主机',
                'edit_action': '/frontend/cmdb/host_list/%s/host_edit_action/',
                'edit_form_plugin': 'host_edit_form_plugin',
                'add_form_plugin': 'host_add_form_plugin'
            }}),

    # 资产导入
    url(r'assert_import/upload_file/', upload_file),
    url(r'assert_import/$', assert_import_index),

]
