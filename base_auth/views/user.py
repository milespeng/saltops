from braces.views import *
from django.contrib.auth.mixins import *
from django.contrib.auth.models import User
from django.urls import *
from django.views.generic import *

from base_auth.forms import UserForm
from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE

listview_lazy_url = 'base_auth:user_list'
listview_template = 'base_auth/user_list.html'
formview_template = 'base_auth/user_form.html'


class UserView(LoginRequiredMixin,
               OrderableListMixin,
               ListView):
    model = User
    orderable_columns_default = 'id'
    orderable_columns = ['username', 'groups', 'email', 'is_active']
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class UserDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            User.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
