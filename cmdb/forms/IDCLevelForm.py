from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class IDCLevelForm(forms.ModelForm):
    class Meta:
        model = IDCLevel
        fields = ['name', 'comment']


class IDCLevelListFilterForm(forms.Form):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': FORM_WIDGET_BASE_STYLE,
                                                         'placeholder': '名称'
                                                         }))
