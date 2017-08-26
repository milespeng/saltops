from django import forms

from common.constants import FORM_WIDGET_BASE_STYLE
from deploy_manager.models import ProjectModule, Project, ProjectVersion


class ProjectModuleForm(forms.ModelForm):
    class Meta:
        model = ProjectModule
        fields = ['parent', 'name']


class ProjectModuleListFilterForm(forms.Form):
    parent = forms.ModelChoiceField(
        required=False,
        queryset=ProjectModule.objects,
        empty_label='上级业务',
        widget=forms.Select({'class': FORM_WIDGET_BASE_STYLE}))
