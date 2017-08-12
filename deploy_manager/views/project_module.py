from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from deploy_manager.forms import ProjectModuleForm
from deploy_manager.models import *
from saltops.settings import PER_PAGE

listview_lazy_url = 'deploy_manager:project_module_list'
listview_template = 'deploy_manager/project_module_list.html'
formview_template = 'deploy_manager/project_module_form.html'


class ProjectModuleView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = ProjectModule
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'parent', 'create_time', 'update_time']

    def get_queryset(self):
        result_list = ProjectModule.objects.all()
        parent = self.request.GET.get('parent')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)
        if parent:
            result_list = result_list.filter(parent=parent)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(ProjectModuleView, self).get_context_data(**kwargs)
        context['parent'] = self.request.GET.get('parent', '')
        context['project_module'] = ProjectModule.objects.filter(parent=None).all()
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        return context


class ProjectModuleCreateView(LoginRequiredMixin, CreateView):
    model = ProjectModule
    form_class = ProjectModuleForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class ProjectModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectModule
    form_class = ProjectModuleForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class ProjectModuleDeleteView(LoginRequiredMixin, JSONResponseMixin,
                              AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            ProjectModule.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
