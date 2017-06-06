from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from deploy_manager.forms import ProjectModuleForm
from deploy_manager.models import *
from saltops.settings import PER_PAGE


class ProjectModuleView(LoginRequiredMixin, ListView):
    model = ProjectModule
    paginate_by = PER_PAGE
    template_name = 'deploy_manager/project_module_list.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        result_list = ProjectModule.objects.all()
        parent = self.request.GET.get('parent')
        if parent:
            result_list = result_list.filter(parent=parent)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(ProjectModuleView, self).get_context_data(**kwargs)
        context['parent'] = self.request.GET.get('parent', '')
        context['project_module'] = ProjectModule.objects.filter(parent=None).all()

        return context


class ProjectModuleCreateView(LoginRequiredMixin, CreateView):
    model = ProjectModule
    form_class = ProjectModuleForm
    template_name = 'deploy_manager/project_module_form.html'
    success_url = reverse_lazy('deploy_manager:project_module_list')


class ProjectModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectModule
    form_class = ProjectModuleForm
    template_name = 'deploy_manager/project_module_form.html'
    success_url = reverse_lazy('deploy_manager:project_module_list')


class ProjectModuleDeleteView(LoginRequiredMixin, JSONResponseMixin,
                              AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            ProjectModule.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
