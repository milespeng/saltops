from django import forms

from common.constants import FORM_WIDGET_BASE_STYLE
from deploy_manager.models import ProjectModule, Project, ProjectVersion


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='业务名称')


class ProjectVersionForm(forms.ModelForm):
    class Meta:
        model = ProjectVersion
        fields = ['project', 'name', 'files', 'software_files']
