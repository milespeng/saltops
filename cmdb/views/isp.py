from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE


class ISPView(LoginRequiredMixin, ListView):
    model = ISP
    paginate_by = PER_PAGE
    template_name = 'cmdb/isp_list.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        result_list = ISP.objects.all()
        name = self.request.GET.get('name')
        if name:
            result_list = result_list.filter(name__contains=name)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(ISPView, self).get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        return context


class ISPCreateView(LoginRequiredMixin, CreateView):
    model = ISP
    form_class = ISPForm
    template_name = 'cmdb/isp_form.html'
    success_url = reverse_lazy('cmdb:isp_list')


class ISPUpdateView(LoginRequiredMixin, UpdateView):
    model = ISP
    form_class = ISPForm
    template_name = 'cmdb/isp_form.html'
    success_url = reverse_lazy('cmdb:isp_list')


class ISPDeleteView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            ISP.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
