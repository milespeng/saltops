from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['idc', 'name']


class CabinetListFilterForm(forms.Form):
    idc = forms.ModelChoiceField(
        queryset=IDC.objects, required=False, empty_label='机房类型')
    name = forms.CharField(required=False, label='机柜')
