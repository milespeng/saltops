from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = '__all__'


class HostListFilterForm(forms.Form):
    ip_filter = forms.CharField(
        required=False, label='IP')
    host_group = forms.ModelChoiceField(
        queryset=HostGroup.objects,
        empty_label='主机组', required=False)
    host = forms.CharField(required=False, label='主机名')
