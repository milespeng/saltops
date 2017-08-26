from django import forms

from common.constants import FORM_WIDGET_BASE_STYLE
from deploy_manager.models import ProjectModule, Project, ProjectVersion


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_module', 'name',
                  'dev_monitor', 'ops_monitor',
                  'backup_monitor']


class ProjectListFilterForm(forms.Form):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': FORM_WIDGET_BASE_STYLE,
                                                         'placeholder': '业务名称'
                                                         }))


class ProjectVersionForm(forms.ModelForm):
    class Meta:
        model = ProjectVersion
        fields = ['project', 'name', 'files', 'software_files']
