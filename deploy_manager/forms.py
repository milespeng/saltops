from django import forms

from deploy_manager.models import ProjectModule, Project, ProjectVersion


class ProjectModuleForm(forms.ModelForm):
    class Meta:
        model = ProjectModule
        fields = ['parent', 'name']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_module', 'name',
                  'dev_monitor', 'ops_monitor',
                  'backup_monitor']


class ProjectVersionForm(forms.ModelForm):
    class Meta:
        model = ProjectVersion
        fields = ['project', 'name', 'files', 'software_files']
