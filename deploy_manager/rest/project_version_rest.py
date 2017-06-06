from braces.views import JSONResponseMixin, AjaxResponseMixin, CsrfExemptMixin
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework.decorators import api_view

from deploy_manager.models import ProjectVersion, Project


# @api_view(['POST'])
# def ProjectVersionUpdateRest(request, project_name, project_version_name):
#     project_file = request.FILES.get("file", None)
#     if project_file:
#         project = Project.objects.get_or_create(name=project_name)
#         project_version = ProjectVersion.objects.get_or_create(project=project[0],
#                                                                name=project_version_name)
#         project_version[0].files = project_file
#         project_version[0].save()
#     return HttpResponse("")


# curl http://127.0.0.1:8000/frontend/deploy_manager/project_list/username/password/11/2232/project_version_update_rest/ -F "file=@/home/kira/sources.list"
@csrf_exempt
def ProjectVersionUpdateRest(request,
                             project_name,
                             project_version_name,
                             username,
                             password):
    user = auth.authenticate(username=username, password=password)
    if user and user.is_active:
        project_file = request.FILES.get("file", None)
        if project_file:
            project = Project.objects.get_or_create(name=project_name)
            project_version = ProjectVersion.objects.get_or_create(project=project[0],
                                                                   name=project_version_name)
            project_version[0].files = project_file
            project_version[0].save()
            return HttpResponse("")
        else:
            return HttpResponse("")
    else:
        return HttpResponse("")

# class ProjectVersionUpdateRestView(JSONResponseMixin,
#                                    CsrfExemptMixin,
#                                    AjaxResponseMixin, View):
#     def post_ajax(self, request, *args, **kwargs):
#         project_name = request.POST.get('name')
#         project_version_name = request.POST.get('project_version_name')
#         project_file = request.FILES.get("file", None)
#         if project_name and project_version_name and project_file:
#             project = Project.objects.get(name=project_name)
#             if project is not None:
#                 # 更新版本
#                 ProjectVersion(
#                     name=project_version_name,
#                     files=project_file,
#                     project=project
#                 ).save()
#                 return self.render_json_response({"success": True})
#             else:
#                 new_project = Project(name=project_name)
#                 new_project.save()
#                 ProjectVersion(
#                     name=project_version_name,
#                     files=project_file,
#                     project=new_project
#                 ).save()
#                 return self.render_json_response({"success": True})
#
#         else:
#             return self.render_json_response({"success": False})
