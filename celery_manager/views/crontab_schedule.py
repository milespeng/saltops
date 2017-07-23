from braces.views import *
from django.contrib.auth.mixins import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import *
from django.views.generic import *
from djcelery.models import CrontabSchedule
from celery_manager.forms import *
from saltops.settings import PER_PAGE
from django.contrib import messages

listview_lazy_url = 'celery_manager:crontab_schedule_list'
listview_template = 'celery_manager/crontab_schedule_list.html'
formview_template = 'celery_manager/crontab_schedule_form.html'


class CrontabScheduleView(LoginRequiredMixin,
                          OrderableListMixin,
                          ListView):
    model = CrontabSchedule
    paginate_by = PER_PAGE
    orderable_columns = CrontabSchedule._meta.ordering
    orderable_columns_default = "id"
    template_name = listview_template
    context_object_name = 'result_list'


class CrontabScheduleCreateView(SuccessMessageMixin,
                                LoginRequiredMixin, CreateView):
    model = CrontabSchedule
    form_class = CrontabScheduleForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    success_message = "新增成功"


class CrontabScheduleUpdateView(SuccessMessageMixin,
                                LoginRequiredMixin, UpdateView):
    model = CrontabSchedule
    form_class = CrontabScheduleForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    success_message = "编辑成功"


class CrontabScheduleDeleteView(LoginRequiredMixin, JSONResponseMixin,
                                AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            CrontabSchedule.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
