from django import forms

from tools_manager.models import *


class ToolsTypesForm(forms.ModelForm):
    class Meta:
        model = ToolsTypes
        fields = '__all__'
