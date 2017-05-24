from django import forms

from cmdb.models import IDCLevel


class IDCLevelForm(forms.ModelForm):
    class Meta:
        model = IDCLevel
        fields = ['name', 'comment']
        help_texts = {
            'name': '*'
        }
