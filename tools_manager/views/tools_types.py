from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from saltops.settings import PER_PAGE
from tools_manager.forms import *
from tools_manager.models import *


class ToolsTypesView(LoginRequiredMixin, ListView):
    model = ToolsTypes
    paginate_by = PER_PAGE
    template_name = 'tools_manager/tools_types_list.html'
    context_object_name = 'result_list'


class ToolsTypesCreateView(LoginRequiredMixin, CreateView):
    model = ToolsTypes
    form_class = ToolsTypesForm
    template_name = 'tools_manager/tools_types_form.html'
    success_url = reverse_lazy('tools_manager:tools_types_list')


class ToolsTypesUpdateView(LoginRequiredMixin, UpdateView):
    model = ToolsTypes
    form_class = ToolsTypesForm
    template_name = 'tools_manager/tools_types_form.html'
    success_url = reverse_lazy('tools_manager:tools_types_list')


class ToolsTypesDeleteView(LoginRequiredMixin, JSONResponseMixin,
                           AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            ToolsTypes.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
