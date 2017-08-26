from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.forms.IDCForm import IDCForm
from cmdb.models import *
from saltops.settings import PER_PAGE

listview_lazy_url = 'cmdb:idc_list'
listview_template = 'cmdb/idc_list.html'
formview_template = 'cmdb/idc_form.html'


class IDCView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = IDC
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'type', 'phone', 'linkman', 'address', 'operator', 'concat_email', 'create_time',
                         'update_time']

    def get_queryset(self):
        result_list = IDC.objects.all()
        operator = self.request.GET.get('operator')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)
        if operator:
            result_list = result_list.filter(operator=operator)

        return result_list

    def get_context_data(self, **kwargs):
        context = super(IDCView, self).get_context_data(**kwargs)
        context['operator'] = self.request.GET.get('operator', '')
        context['isp_type'] = ISP.objects.all()
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        return context


class IDCCreateView(LoginRequiredMixin, CreateView):
    model = IDC
    form_class = IDCForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class IDCUpdateView(LoginRequiredMixin, UpdateView):
    model = IDC
    form_class = IDCForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class IDCDeleteView(LoginRequiredMixin, JSONResponseMixin,
                    AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            IDC.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
