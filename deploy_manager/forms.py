from django import forms

from deploy_manager.models import ProjectModule, Project, ProjectVersion


class ProjectModuleForm(forms.ModelForm):
    class Meta:
        model = ProjectModule
        fields = ['parent', 'name']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_module', 'name', 'job_script_type',
                  'playbook', 'anti_install_playbook',
                  'extra_param', 'dev_monitor', 'ops_monitor',
                  'backup_monitor']


class ProjectVersionForm(forms.ModelForm):
    class Meta:
        model = ProjectVersion
        fields = ['project', 'name', 'files', 'is_default', 'subplaybook',
                  'sub_job_script_type', 'extra_param', 'anti_install_playbook']
