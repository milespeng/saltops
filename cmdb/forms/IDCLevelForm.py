from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class IDCLevelForm(forms.ModelForm):
    class Meta:
        model = IDCLevel
        fields = '__all__'


class IDCLevelListFilterForm(forms.Form):
    name = forms.CharField(required=False,label='机房等级')
