from braces.views import JSONResponseMixin, AjaxResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from cmdb.forms import IDCLevelForm
from cmdb.models import IDCLevel
from saltops.settings import PER_PAGE


class IDCLevelView(LoginRequiredMixin, ListView):
    model = IDCLevel
    paginate_by = PER_PAGE
    template_name = 'cmdb/idc_level_list.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        result_list = IDCLevel.objects.all()
        name = self.request.GET.get('name')
        if name:
            result_list = result_list.filter(name__contains=name)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(IDCLevelView, self).get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        return context


class IDCLevelCreateView(LoginRequiredMixin, CreateView):
    model = IDCLevel
    form_class = IDCLevelForm
    template_name = 'cmdb/idc_level_form.html'
    success_url = reverse_lazy('cmdb:idc_level_list')


class IDCLevelUpdateView(LoginRequiredMixin, UpdateView):
    model = IDCLevel
    form_class = IDCLevelForm
    template_name = 'cmdb/idc_level_form.html'
    success_url = reverse_lazy('cmdb:idc_level_list')


class IDCLevelDeleteView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            IDCLevel.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
