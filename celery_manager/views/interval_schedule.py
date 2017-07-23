from braces.views import *
from django.contrib.auth.mixins import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import *
from django.views.generic import *
from djcelery.models import IntervalSchedule
from django.contrib import messages
from celery_manager.forms import *
from saltops.settings import PER_PAGE

listview_lazy_url = 'celery_manager:interval_schedule_list'
listview_template = 'celery_manager/interval_schedule_list.html'
formview_template = 'celery_manager/interval_schedule_form.html'


class IntervalScheduleView(LoginRequiredMixin,
                           OrderableListMixin,
                           ListView):
    orderable_columns_default = 'id'
    orderable_columns = IntervalSchedule._meta.ordering
    model = IntervalSchedule
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'


class IntervalScheduleCreateView(SuccessMessageMixin,
                                 LoginRequiredMixin, CreateView):
    model = IntervalSchedule
    form_class = IntervalScheduleForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    success_message = "新增成功"


class IntervalScheduleUpdateView(SuccessMessageMixin,
                                 LoginRequiredMixin, UpdateView):
    model = IntervalSchedule
    form_class = IntervalScheduleForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    success_message = "编辑成功"


class IntervalScheduleDeleteView(LoginRequiredMixin, JSONResponseMixin,
                                 AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            IntervalSchedule.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
