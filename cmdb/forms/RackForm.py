from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = '__all__'


class RackListFilterForm(forms.Form):
    idc = forms.ModelChoiceField(queryset=IDC.objects,
                                 required=False,
                                 empty_label='机房')
