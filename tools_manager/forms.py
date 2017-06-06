from django import forms

from tools_manager.models import *


class ToolsTypesForm(forms.ModelForm):
    class Meta:
        model = ToolsTypes
        fields = ['name']


class ToolsScriptForm(forms.ModelForm):
    class Meta:
        model = ToolsScript
        fields = ['name', 'tool_script', 'tools_type', 'tool_run_type',
                  'comment']
