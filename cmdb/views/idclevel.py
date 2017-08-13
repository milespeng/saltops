from braces.views import JSONResponseMixin, AjaxResponseMixin, OrderableListMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from cmdb.forms import IDCLevelForm
from cmdb.models import IDCLevel
from saltops.settings import PER_PAGE

listview_lazy_url = 'cmdb:idc_level_list'
listview_template = 'cmdb/idc_level_list.html'
formview_template = 'cmdb/idc_level_form.html'


class IDCLevelView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = IDCLevel
    paginate_by = PER_PAGE
    template_name = listview_template
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'comment', 'create_time', 'update_time']
    context_object_name = 'result_list'

    def get_queryset(self):
        result_list = IDCLevel.objects.all()
        name = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)
        if name:
            result_list = result_list.filter(name__contains=name)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(IDCLevelView, self).get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        return context


class IDCLevelCreateView(LoginRequiredMixin, CreateView):
    model = IDCLevel
    form_class = IDCLevelForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class IDCLevelUpdateView(LoginRequiredMixin, UpdateView):
    model = IDCLevel
    form_class = IDCLevelForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)


class IDCLevelDeleteView(LoginRequiredMixin, JSONResponseMixin,
                         AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            IDCLevel.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
