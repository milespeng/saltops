from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *
from djcelery.models import IntervalSchedule

from celery_manager.forms import *
from saltops.settings import PER_PAGE


class IntervalScheduleView(LoginRequiredMixin, ListView):
    model = IntervalSchedule
    paginate_by = PER_PAGE
    template_name = 'celery_manager/interval_schedule_list.html'
    context_object_name = 'result_list'


class IntervalScheduleCreateView(LoginRequiredMixin, CreateView):
    model = IntervalSchedule
    form_class = IntervalScheduleForm
    template_name = 'celery_manager/interval_schedule_form.html'
    success_url = reverse_lazy('celery_manager:interval_schedule_list')


class IntervalScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = IntervalSchedule
    form_class = IntervalScheduleForm
    template_name = 'celery_manager/interval_schedule_form.html'
    success_url = reverse_lazy('celery_manager:interval_schedule_list')


class IntervalScheduleDeleteView(LoginRequiredMixin, JSONResponseMixin,
                                 AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            IntervalSchedule.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
