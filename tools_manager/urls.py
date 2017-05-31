from django.conf.urls import include, url

from tools_manager.views import *

urlpatterns = [
    # 工具类型
    url(r'^tools_types_list/', include([
        url(r'^delete_entity/', ToolsTypesDeleteView.as_view(), name='tools_types_delete'),
        url(r'^(?P<pk>\d+)/tools_types_edit/', ToolsTypesUpdateView.as_view(), name='tools_types_edit'),
        url(r'^tools_types_add/', ToolsTypesCreateView.as_view(), name='tools_types_add'),
        url(r'^$', ToolsTypesView.as_view(), name='tools_types_list'),
    ])),

    url(r'^tools_script_list/', include([
        url(r'^tool_execute_history/', ToolExecuteHistoryView.as_view()),
        url(r'^tool_execute_action/', ToolExecuteActionView.as_view()),
        url(r'^delete_entity/', ToolsScriptDeleteView.as_view(), name='tools_script_delete'),
        url(r'^^(?P<pk>\d+)/tools_script_edit/', ToolsScriptUpdateView.as_view(), name='tools_script_edit'),
        url(r'^tools_script_add/', ToolsScriptCreateView.as_view(), name='tools_script_add'),
        url(r'^tool_execute/', ToolExecuteView.as_view()),
        url(r'^$', ToolsScriptView.as_view(), name='tools_script_list'),
    ])),

]
