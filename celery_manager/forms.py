from djcelery.admin import TaskChoiceField
from djcelery.models import *
from django import forms
from anyjson import loads


class IntervalScheduleForm(forms.ModelForm):
    class Meta:
        model = IntervalSchedule
        fields = IntervalSchedule._meta.ordering


class CrontabScheduleForm(forms.ModelForm):
    class Meta:
        model = CrontabSchedule
        fields = CrontabSchedule._meta.ordering


class TaskStateForm(forms.ModelForm):
    class Meta:
        model = TaskState
        fields = ['name', 'state', 'task_id', 'tstamp', 'args', 'kwargs',
                  'eta', 'expires', 'result', 'traceback', 'runtime', 'retries', 'worker']


class PeriodicTaskForm(forms.ModelForm):
    regtask = TaskChoiceField(label='计划任务（已注册）',
                              required=False)
    task = forms.CharField(label='计划任务（自定义）', required=False)

    class Meta:
        model = PeriodicTask
        fields = ['name', 'regtask', 'task', 'interval',
                  'crontab', 'args', 'kwargs', 'queue',
                  'exchange', 'routing_key', 'expires',
                  'enabled', 'description']

    def clean(self):
        data = super(PeriodicTaskForm, self).clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError("请填写主机名")
            self._errors['task'] = self.error_class(exc.messages)
            raise exc
        return data

    def _clean_json(self, field):
        value = self.cleaned_data[field]
        try:
            loads(value)
        except ValueError as exc:
            raise forms.ValidationError(
                '解析JSON失败: %s' % exc,
            )
        return value

    def clean_args(self):
        return self._clean_json('args')

    def clean_kwargs(self):
        return self._clean_json('kwargs')
