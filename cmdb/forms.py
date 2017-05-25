from django import forms

from cmdb.models import *


class IDCLevelForm(forms.ModelForm):
    class Meta:
        model = IDCLevel
        fields = ['name', 'comment']


class ISPForm(forms.ModelForm):
    class Meta:
        model = ISP
        fields = ['name']


class IDCForm(forms.ModelForm):
    class Meta:
        model = IDC
        fields = ['name', 'operator', 'bandwidth', 'phone', 'linkman',
                  'address', 'concat_email', 'network',
                  'type', 'comment']


class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['idc', 'name']
