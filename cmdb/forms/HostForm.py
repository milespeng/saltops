from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = '__all__'


class HostListFilterForm(forms.Form):
    ip_filter = forms.CharField(
        required=False,
        widget=forms.TextInput({'class': FORM_WIDGET_BASE_STYLE, 'placeholder': 'IP'}))
    host_group = forms.ModelChoiceField(
        queryset=HostGroup.objects,
        empty_label='主机组', required=False,
        widget=forms.Select({'class': FORM_WIDGET_BASE_STYLE}))
    host = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': FORM_WIDGET_BASE_STYLE,
               'placeholder': '主机名'
               }))
