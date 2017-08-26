from django import forms

from cmdb.models import *
from common.constants import FORM_WIDGET_BASE_STYLE


class ISPForm(forms.ModelForm):
    class Meta:
        model = ISP
        fields = ['name']


class ISPListFilterForm(forms.Form):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': FORM_WIDGET_BASE_STYLE,
                                                         'placeholder': 'ISP名称'
                                                         }))
