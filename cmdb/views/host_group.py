from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE

listview_lazy_url = 'cmdb:hostgroup_list'
listview_template = 'cmdb/hostgroup_list.html'
formview_template = 'cmdb/hostgroup_form.html'


class HostGroupView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = HostGroup
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['host_group', 'host_name', 'create_time', 'update_time']


class HostGroupCreateView(LoginRequiredMixin, CreateView):
    model = HostGroup
    form_class = HostGroupForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class HostGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = HostGroup
    form_class = HostGroupForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class HostGroupDeleteView(LoginRequiredMixin, JSONResponseMixin,
                          AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            HostGroup.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
