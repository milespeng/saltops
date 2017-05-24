from django.views.generic import ListView

from cmdb.models import IDC, IDCLevel
from saltops.settings import PER_PAGE


class IDCLevelView(ListView):
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
