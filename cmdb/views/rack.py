from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE


class RackView(LoginRequiredMixin, ListView):
    model = Rack
    paginate_by = PER_PAGE
    template_name = 'cmdb/rack_list.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        result_list = Rack.objects.all()
        idc = self.request.GET.get('idc')
        if idc:
            result_list = result_list.filter(idc_id=int(idc))
        return result_list

    def get_context_data(self, **kwargs):
        context = super(RackView, self).get_context_data(**kwargs)
        context['idc'] = self.request.GET.get('idc', '')
        context['idclist'] = IDC.objects.all()
        return context


class RackCreateView(LoginRequiredMixin, CreateView):
    model = Rack
    form_class = RackForm
    template_name = 'cmdb/rack_form.html'
    success_url = reverse_lazy('cmdb:rack_list')
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(RackCreateView, self).get_context_data(**kwargs)
        context['is_add'] = True
        return context


class RackUpdateView(LoginRequiredMixin, UpdateView):
    model = Rack
    form_class = RackForm
    template_name = 'cmdb/rack_form.html'
    success_url = reverse_lazy('cmdb:rack_list')
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(RackCreateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        context['cabinet_list'] = Cabinet.objects.all()
        return context


class RackDeleteView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Rack.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})


class LoadCabinetListView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result = Cabinet.objects.filter(idc=int(request.GET.get('idc_id')))
        return self.render_json_object_response(result)


class LoadRackListView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        result = Rack.objects.filter(idc=int(request.GET.get('idc_id')),
                                     cabinet=int(request.GET.get('cabinet_id')))
        return self.render_json_object_response(result)
