from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE


class IDCView(LoginRequiredMixin, ListView):
    model = IDC
    paginate_by = PER_PAGE
    template_name = 'cmdb/idc_list.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        result_list = IDC.objects.all()
        operator = self.request.GET.get('operator')
        if operator:
            result_list = result_list.filter(operator=operator)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(IDCView, self).get_context_data(**kwargs)
        context['operator'] = self.request.GET.get('operator', '')
        context['isp_type'] = ISP.objects.all()
        return context


class IDCCreateView(LoginRequiredMixin, CreateView):
    model = IDC
    form_class = IDCForm
    template_name = 'cmdb/idc_form.html'
    success_url = reverse_lazy('cmdb:idc_list')


class IDCUpdateView(LoginRequiredMixin, UpdateView):
    model = IDC
    form_class = IDCForm
    template_name = 'cmdb/idc_form.html'
    success_url = reverse_lazy('cmdb:idc_list')


class IDCDeleteView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            IDC.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
