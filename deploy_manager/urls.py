from django.conf.urls import include, url

# from deploy_manager.rest.project_version_rest import ProjectVersionUpdateRest
from deploy_manager.rest.project_version_rest import ProjectVersionUpdateRest
from deploy_manager.views import *

urlpatterns = [
    # 业务模块
    url(r'^project_module_list/', include([
        url(r'^delete_entity/', ProjectModuleDeleteView.as_view(), name='project_module_delete'),
        url(r'^(?P<pk>\d+)/project_module_edit/', ProjectModuleUpdateView.as_view(), name='project_module_edit'),
        url(r'^project_module_add/', ProjectModuleCreateView.as_view(), name='project_module_add'),
        url(r'^$', ProjectModuleView.as_view(), name='project_module_list'),
    ])),

    # 业务
    url(r'^project_list/', include([
        url(r'^project_deploy_history/', ProjectDeployHistoryView.as_view()),
        url(r'^delete_entity/', ProjectDeleteView.as_view(), name='project_delete'),
        url(r'^(?P<pk>\d+)/project_edit/', ProjectUpdateView.as_view(), name='project_edit'),
        url(r'^project_add/', ProjectCreateView.as_view(), name='project_add'),
        url(r'^project_version/', ProjectVersionCreateView.as_view()),
        url(r'^(?P<pk>\d+)/project_version_edit/', ProjectVersionUpdateView.as_view()),
        url(r'delete_project_version/', ProjectVersionDeleteView.as_view()),
        url(r'project_deploy_action/', ProjectDeployActionView.as_view()),
        url(r'project_hostgroup_undeploy_action/',
            ProjectHostGroupUnDeployActionView.as_view()),
        url(r'project_host_undeploy_action/',
            ProjectHostUnDeployActionView.as_view()),
        url(r'project_host_start_action/',
            ProjectHostStartActionView.as_view()),
        url(r'project_host_stop_action/',
            ProjectHostStopActionView.as_view()),
        url(r'project_deploy/', ProjectDeployView.as_view()),
        url(
            r'^(?P<username>\w+)/(?P<password>\w+)/(?P<project_name>\w+)/(?P<project_version_name>\w+)/project_version_update_rest/',
            ProjectVersionUpdateRest),
        url(r'^$', ProjectView.as_view(), name='project_list'),
    ]))
]
