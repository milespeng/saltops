from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE

listview_lazy_url = 'cmdb:cabinet_list'
listview_template = 'cmdb/cabinet_list.html'
formview_template = 'cmdb/cabinet_form.html'


class CabinetView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Cabinet
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'idc', 'create_time', 'update_time']

    def get_queryset(self):
        result_list = Cabinet.objects.all()
        idc = self.request.GET.get('idc')
        name = self.request.GET.get('name')
        if idc:
            result_list = result_list.filter(idc_id=int(idc))
        if name:
            result_list = result_list.filter(name__contains=name)
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(CabinetView, self).get_context_data(**kwargs)
        context['idc'] = self.request.GET.get('idc', '')
        context['idclist'] = IDC.objects.all()
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = CabinetListFilterForm(self.request.GET)
        return context


class CabinetCreateView(LoginRequiredMixin, CreateView):
    model = Cabinet
    form_class = CabinetForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class CabinetUpdateView(LoginRequiredMixin, UpdateView):
    model = Cabinet
    form_class = CabinetForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class CabinetDeleteView(LoginRequiredMixin, JSONResponseMixin,
                        AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Cabinet.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
