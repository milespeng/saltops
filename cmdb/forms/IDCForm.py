from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class IDCForm(forms.ModelForm):
    class Meta:
        model = IDC
        fields = '__all__'
