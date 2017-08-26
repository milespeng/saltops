from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class HostGroupForm(forms.ModelForm):
    class Meta:
        model = HostGroup
        fields = '__all__'
