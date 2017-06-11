from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *
from celery_manager.forms import *
from saltops.settings import PER_PAGE


class PeriodicTaskView(LoginRequiredMixin, ListView):
    model = PeriodicTask
    paginate_by = PER_PAGE
    template_name = 'celery_manager/preriodic_task_list.html'
    context_object_name = 'result_list'


class PeriodicTaskCreateView(LoginRequiredMixin, CreateView):
    model = PeriodicTask
    form_class = PeriodicTaskForm
    template_name = 'celery_manager/preriodic_task_form.html'
    success_url = reverse_lazy('celery_manager:preriodic_task_list')


class PeriodicTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = PeriodicTask
    form_class = PeriodicTaskForm
    template_name = 'celery_manager/preriodic_task_form.html'
    success_url = reverse_lazy('celery_manager:preriodic_task_list')


class PeriodicTaskDeleteView(LoginRequiredMixin, JSONResponseMixin,
                                 AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            PeriodicTask.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
