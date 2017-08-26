from django import forms

from common.constants import FORM_WIDGET_BASE_STYLE
from tools_manager.models import *


class ToolsScriptForm(forms.ModelForm):
    class Meta:
        model = ToolsScript
        fields = ['name', 'tool_script', 'tools_type', 'tool_run_type',
                  'comment']


# TODO:这里应该优化，从原有的脚本类型里面追加一条记录才合适
TOOL_RUN_TYPE_FILTER = (
    (None, '脚本类型'),
    (0, 'SaltState'),
    (1, 'Shell'),
    (2, 'PowerShell'),
    (3, 'Python'),
    (4, 'Salt命令'),
    (5, 'Windows批处理')
)


class ToolsScriptListFilterForm(forms.Form):
    tools_type = forms.ModelChoiceField(
        required=False,
        queryset=ToolsTypes.objects,
        empty_label='工具类型',
        widget=forms.Select({'class': FORM_WIDGET_BASE_STYLE}))
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': FORM_WIDGET_BASE_STYLE,
               'placeholder': '工具名称'
               }))
    tool_run_type = forms.ChoiceField(
        choices=TOOL_RUN_TYPE_FILTER,
        required=False,
        widget=forms.Select({'class': FORM_WIDGET_BASE_STYLE}))
