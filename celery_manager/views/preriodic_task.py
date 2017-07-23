from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *
from celery_manager.forms import *
from saltops.settings import PER_PAGE
from django.contrib import messages

listview_lazy_url = 'celery_manager:preriodic_task_list'
listview_template = 'celery_manager/preriodic_task_list.html'
formview_template = 'celery_manager/preriodic_task_form.html'


class PeriodicTaskView(LoginRequiredMixin,
                       OrderableListMixin,
                       ListView):
    orderable_columns_default = 'id'
    orderable_columns = ('name', 'regtask', 'task', 'interval',
                         'crontab', 'args', 'kwargs', 'queue',
                         'exchange', 'routing_key', 'expires',
                         'enabled', 'description')
    model = PeriodicTask
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'


class PeriodicTaskCreateView(LoginRequiredMixin, CreateView):
    model = PeriodicTask
    form_class = PeriodicTaskForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def form_valid(self, form):
        messages.success(self.request, "新增成功")
        return super(PeriodicTaskCreateView, self).form_valid(form)


class PeriodicTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = PeriodicTask
    form_class = PeriodicTaskForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def form_valid(self, form):
        messages.success(self.request, "编辑成功")
        return super(PeriodicTaskUpdateView, self).form_valid(form)


class PeriodicTaskDeleteView(LoginRequiredMixin, JSONResponseMixin,
                             AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            PeriodicTask.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
