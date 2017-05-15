from django.conf.urls import include, url

from deploy_manager.c_views import *
from common import views
from common.common_views import *

urlpatterns = [
    # 业务模块
    url(r'^project_module_list/', include([
        url(r'(?P<pk>\d+)/project_module_edit_action/', simple_edit_action),
        url(r'(?P<pk>\d+)/project_module_edit/', simple_edit),
        url(r'project_module_add_action/', simple_add_action),
        url(r'project_module_add/', simple_add),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'args': {
                'modulename': 'deploy_manager.models',
                'modelname': 'ProjectModule',
                'list_url': '/frontend/deploy_manager/project_module_list/',
                'form_template_path': 'frontend/common/basic_form.html',
                'template_path': 'frontend/deploy_manager/project_module_list.html',
                'add_title': '新增业务模块',
                'add_action': '/frontend/deploy_manager/project_module_list/project_module_add_action/',
                'edit_title': '编辑业务模块',
                'edit_action': '/frontend/deploy_manager/project_module_list/%s/project_module_edit_action/',
                'plugin_name': 'project_module_list_plugin'
            }
        }),

    url(r'^project_list/(?P<pk>\d+)/project_version', project_version),
    # 业务
    url(r'^project_list/', include([
        url(r'(?P<pk>\d+)/project_edit_action/', simple_edit_action),
        url(r'(?P<pk>\d+)/project_edit/', simple_edit),
        url(r'project_add_action/', project_add_action),
        url(r'project_add/', simple_add),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'args': {
                'modulename': 'deploy_manager.models',
                'modelname': 'Project',
                'list_url': '/frontend/deploy_manager/project_list/',
                'form_template_path': 'frontend/deploy_manager/project_form.html',
                'template_path': 'frontend/deploy_manager/project_list.html',
                'add_title': '新增业务',
                'add_action': '/frontend/deploy_manager/project_list/project_add_action/',
                'edit_title': '编辑业务',
                'edit_action': '/frontend/deploy_manager/project_list/%s/project_edit_action/',
                'add_form_plugin': 'add_form_plugin'
                # 'plugin_name': 'project_list_plugin'
            }
        }),
]
