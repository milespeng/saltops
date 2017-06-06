from braces.views import *
from django.contrib.auth.mixins import *
from django.contrib.auth.models import User
from django.urls import *
from django.views.generic import *

from base_auth.forms import UserForm
from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE


class UserView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = PER_PAGE
    template_name = 'base_auth/user_list.html'
    context_object_name = 'result_list'



class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'base_auth/user_form.html'
    success_url = reverse_lazy('base_auth:user_list')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'base_auth/user_form.html'
    success_url = reverse_lazy('base_auth:user_list')


class UserDeleteView(LoginRequiredMixin, JSONResponseMixin,
                      AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            User.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
