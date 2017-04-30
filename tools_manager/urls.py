from django.conf.urls import include, url

from tools_manager.c_views import *
from common import views
from common.common_views import *

urlpatterns = [
    # 工具类型
    url(r'^tools_types_list/', include([
        url(r'(?P<pk>\d+)/tools_types_edit_action/', simple_edit_action),
        url(r'(?P<pk>\d+)/tools_types_edit/', simple_edit),
        url(r'tools_types_add_action/', simple_add_action),
        url(r'tools_types_add/', simple_add),
        url(r'(?P<pk>\d+)/delete_entity/', simple_delete_entity),
        url(r'batch_delete_entity/', simple_batch_delete_entity),
        url(r'$', simple_list),
    ]), {
            'args': {
                'modulename': 'tools_manager.models',
                'modelname': 'ToolsTypes',
                'list_url': '/frontend/tools_manager/tools_types_list/',
                'form_template_path': 'frontend/common/basic_form.html',
                'template_path': 'frontend/tools_manager/tools_types_list.html',
                'add_title': '新增工具类型',
                'add_action': '/frontend/tools_manager/tools_types_list/tools_types_add_action/',
                'edit_title': '编辑工具类型',
                'edit_action': '/frontend/tools_manager/tools_types_list/%s/tools_types_edit_action/',
            }
        }),

]