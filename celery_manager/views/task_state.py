from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *
from celery_manager.forms import *
from saltops.settings import PER_PAGE


class TaskStateView(LoginRequiredMixin, ListView):
    model = TaskState
    paginate_by = PER_PAGE
    template_name = 'celery_manager/task_state_list.html'
    context_object_name = 'result_list'


class TaskStateCreateView(LoginRequiredMixin, CreateView):
    model = TaskState
    form_class = TaskStateForm
    template_name = 'celery_manager/task_state_form.html'
    success_url = reverse_lazy('celery_manager:task_state_list')


class TaskStateUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskState
    form_class = TaskStateForm
    template_name = 'celery_manager/task_state_form.html'
    success_url = reverse_lazy('celery_manager:task_state_list')


class TaskStateDeleteView(LoginRequiredMixin, JSONResponseMixin,
                                 AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            TaskState.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
