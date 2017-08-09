from braces.views import *
from django.contrib.auth.mixins import *
from django.contrib.auth.models import Group
from django.urls import *
from django.views.generic import *

from base_auth.forms import GroupForm
from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE

listview_lazy_url = 'base_auth:group_list'
listview_template = 'base_auth/groups_list.html'
formview_template = 'base_auth/groups_form.html'


class GroupView(LoginRequiredMixin,
                OrderableListMixin,
                ListView):
    model = Group
    paginate_by = PER_PAGE
    orderable_columns_default = 'id'
    orderable_columns = ['name']
    template_name = listview_template
    context_object_name = 'result_list'


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class GroupDeleteView(LoginRequiredMixin, JSONResponseMixin,
                      AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Group.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
