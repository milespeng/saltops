from deploy_manager.models import ProjectModule


def project_module_list_plugin():
    project_module = ProjectModule.objects.filter(parent=None).all()
    return {'project_module': project_module}
