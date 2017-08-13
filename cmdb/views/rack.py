from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE


class RackView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Rack
    paginate_by = PER_PAGE
    template_name = 'cmdb/rack_list.html'
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['idc', 'cabinet', 'name', 'create_time', 'update_time']

    def get_queryset(self):
        result_list = Rack.objects.all()
        idc = self.request.GET.get('idc')
        if idc:
            result_list = result_list.filter(idc_id=int(idc))
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(RackView, self).get_context_data(**kwargs)
        context['idc'] = self.request.GET.get('idc', '')
        context['idclist'] = IDC.objects.all()
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
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


class RackDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Rack.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})


class LoadCabinetListView(LoginRequiredMixin, JSONResponseMixin,
                          AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        idc_id = request.GET.get('idc_id')
        if idc_id:
            result = Cabinet.objects.filter(idc=int(idc_id))
        return self.render_json_object_response(result)


class LoadRackListView(LoginRequiredMixin, JSONResponseMixin,
                       AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        idc_id = request.GET.get('idc_id')
        cabinet_id = request.GET.get('cabinet_id')
        result = Rack.objects.filter(idc=int(idc_id),
                                     cabinet=int(cabinet_id))
        return self.render_json_object_response(result)
