from django.conf.urls import include, url

from cmdb.c_views import *
from cmdb.views import *
from common.common_views import *

urlpatterns = [
    # 机房等级

    url(r'^idc_level_list/', include([
        url(r'^delete_entity/', IDCLevelDeleteView.as_view(), name='idc_level_delete'),
        url(r'^(?P<pk>\d+)/idc_level_edit/', IDCLevelUpdateView.as_view(), name='idc_level_edit'),
        url(r'^idc_level_add/', IDCLevelCreateView.as_view(), name='idc_level_add'),
        url(r'^$', IDCLevelView.as_view(), name='idc_level_list'),
    ])),

    # ISP
    url(r'^isp_list/', include([
        url(r'^delete_entity/', ISPDeleteView.as_view(), name='isp_delete'),
        url(r'^(?P<pk>\d+)/isp_edit/', ISPUpdateView.as_view(), name='isp_edit'),
        url(r'^isp_add/', ISPCreateView.as_view(), name='isp_add'),
        url(r'^$', ISPView.as_view(), name='isp_list'),
    ])),

    # IDC
    url(r'^idc_list/', include([
        url(r'^delete_entity/', IDCDeleteView.as_view(), name='idc_delete'),
        url(r'^(?P<pk>\d+)/idc_edit/', IDCUpdateView.as_view(), name='idc_edit'),
        url(r'^idc_add/', IDCCreateView.as_view(), name='idc_add'),
        url(r'^$', IDCView.as_view(), name='idc_list'),
    ])),

    # 机柜
    url(r'^cabinet_list/', include([
        url(r'^delete_entity/', CabinetDeleteView.as_view(), name='cabinet_delete'),
        url(r'^(?P<pk>\d+)/cabinet_edit/', CabinetUpdateView.as_view(), name='cabinet_edit'),
        url(r'^cabinet_add/', CabinetCreateView.as_view(), name='cabinet_add'),
        url(r'^$', CabinetView.as_view(), name='cabinet_list'),
    ])),

    # 机架
    url('^rack_list/', include([
        url(r'^load_cabinet_list/', LoadCabinetListView.as_view(), name='load_cabinet_list'),
        url(r'^load_rack_list/', LoadRackListView.as_view(), 'load_rack_list'),
        url(r'^delete_entity/', RackDeleteView.as_view(), name='rack_delete'),
        url(r'^(?P<pk>\d+)/rack_edit/', RackUpdateView.as_view(), name='rack_edit'),
        url(r'^rack_add/', RackCreateView.as_view(), name='rack_add'),
        url(r'^$', RackView.as_view(), name='rack_list'),
    ])),

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
                'form_template_path': 'common/basic_form.html',
                'template_path': 'cmdb/hostgroup_list.html',
                'add_title': '新增主机组',
                'add_action': '/frontend/cmdb/hostgroup_list/hostgroup_add_action/',
                'edit_title': '编辑主机组',
                'edit_action': '/frontend/cmdb/hostgroup_list/%s/hostgroup_edit_action/',
            }}),

    url(r'host_list/scan_host_job/', scan_host_job),
    # 主机
    url('^host_list/', include([
        url(r'host_add/', simple_add),
        url(r'host_add_action/', host_add_action),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'(?P<pk>\d+)/host_edit/', simple_edit),
        url(r'(?P<pk>\d+)/host_edit_action/', host_edit_action),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', host_list),
    ]), {
            'args': {
                'modulename': 'cmdb.models',
                'modelname': 'Host',
                'list_url': '/frontend/cmdb/host_list/',
                'form_template_path': 'cmdb/host_form.html',
                'template_path': 'cmdb/host_list.html',
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
