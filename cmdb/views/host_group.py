from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE


class HostGroupView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = HostGroup
    paginate_by = PER_PAGE
    template_name = 'cmdb/hostgroup_list.html'
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['host_group', 'host_name', 'create_time', 'update_time']

class HostGroupCreateView(LoginRequiredMixin, CreateView):
    model = HostGroup
    form_class = HostGroupForm
    template_name = 'cmdb/hostgroup_form.html'
    success_url = reverse_lazy('cmdb:hostgroup_list')


class HostGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = HostGroup
    form_class = HostGroupForm
    template_name = 'cmdb/hostgroup_form.html'
    success_url = reverse_lazy('cmdb:hostgroup_list')


class HostGroupDeleteView(LoginRequiredMixin, JSONResponseMixin,
                          AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            HostGroup.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
