from django.conf.urls import include, url

from cmdb.views import *

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
        url(r'^load_cabinet_list/', LoadCabinetListView.as_view()),
        url(r'^load_rack_list/', LoadRackListView.as_view()),
        url(r'^delete_entity/', RackDeleteView.as_view(), name='rack_delete'),
        url(r'^(?P<pk>\d+)/rack_edit/', RackUpdateView.as_view(), name='rack_edit'),
        url(r'^rack_add/', RackCreateView.as_view(), name='rack_add'),
        url(r'^$', RackView.as_view(), name='rack_list'),
    ])),

    # 主机组
    url('^hostgroup_list/', include([
        url(r'^delete_entity/', HostGroupDeleteView.as_view(), name='hostgroup_delete'),
        url(r'^(?P<pk>\d+)/hostgroup_edit/', HostGroupUpdateView.as_view(), name='hostgroup_edit'),
        url(r'^hostgroup_add/', HostGroupCreateView.as_view(), name='hostgroup_add'),
        url(r'^$', HostGroupView.as_view(), name='hostgroup_list'),
    ])),

    # 主机
    url('^host_list/', include([
        url(r'scan_host_job/', ScanHostJobView.as_view()),
        url(r'^delete_entity/', HostDeleteView.as_view(), name='host_delete'),
        url(r'^(?P<pk>\d+)/host_edit/', HostUpdateView.as_view(), name='host_edit'),
        url(r'^host_add/', HostCreateView.as_view(), name='host_add'),
        url(r'^$', HostView.as_view(), name='host_list'),
    ])),

    # 资产导入
    url(r'assert_import/', include([
        url(r'upload_file/', AssertImportView.as_view()),
        url(r'^$', AssertImportCreateView.as_view(), name='assert_import'),
    ])),

]
