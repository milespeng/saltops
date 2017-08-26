from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class ISPForm(forms.ModelForm):
    class Meta:
        model = ISP
        fields = '__all__'


class ISPListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='ISP名称')
