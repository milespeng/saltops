from django import forms

from deploy_manager.models import ProjectModule, Project, ProjectVersion


class ProjectModuleForm(forms.ModelForm):
    class Meta:
        model = ProjectModule
        fields = ['parent', 'name']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_module', 'name', 'install_job_script_type',
                  'install_script', 'anti_install_script_type', 'anti_install_script',
                  'stateguard_script_type', 'stateguard_script',
                  'start_script_type', 'start_script',
                  'stop_script_type', 'stop_script',
                  'state_script_type', 'state_script',
                  'extra_param', 'dev_monitor', 'ops_monitor',
                  'backup_monitor']


class ProjectVersionForm(forms.ModelForm):
    class Meta:
        model = ProjectVersion
        fields = ['project', 'name', 'files', 'is_default',
                  'install_job_script_type',
                  'install_script', 'anti_install_script_type', 'anti_install_script',
                  'stateguard_script_type', 'stateguard_script',
                  'start_script_type', 'start_script',
                  'stop_script_type', 'stop_script',
                  'state_script_type', 'state_script',
                  'extra_param']
