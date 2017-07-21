from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *
from djcelery.models import CrontabSchedule

from celery_manager.forms import *
from saltops.settings import PER_PAGE


class CrontabScheduleView(LoginRequiredMixin,
                          OrderableListMixin,
                          ListView):
    model = CrontabSchedule
    paginate_by = PER_PAGE
    orderable_columns = ('minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')
    orderable_columns_default = "id"
    template_name = 'celery_manager/crontab_schedule_list.html'
    context_object_name = 'result_list'


class CrontabScheduleCreateView(LoginRequiredMixin, CreateView):
    model = CrontabSchedule
    form_class = CrontabScheduleForm
    template_name = 'celery_manager/crontab_schedule_form.html'
    success_url = reverse_lazy('celery_manager:crontab_schedule_list')


class CrontabScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = CrontabSchedule
    form_class = CrontabScheduleForm
    template_name = 'celery_manager/crontab_schedule_form.html'
    success_url = reverse_lazy('celery_manager:crontab_schedule_list')


class CrontabScheduleDeleteView(LoginRequiredMixin, JSONResponseMixin,
                                AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            CrontabSchedule.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
