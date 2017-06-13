from django.conf.urls import include, url

from celery_manager.views import *

urlpatterns = [
    url(r'^interval_schedule_list/', include([
        url(r'^delete_entity/', IntervalScheduleDeleteView.as_view(), name='interval_schedule_delete'),
        url(r'^(?P<pk>\d+)/interval_schedule_edit/', IntervalScheduleUpdateView.as_view(),
            name='interval_schedule_edit'),
        url(r'^interval_schedule_add/', IntervalScheduleCreateView.as_view(), name='interval_schedule_add'),
        url(r'^$', IntervalScheduleView.as_view(), name='interval_schedule_list'),
    ])),
    url(r'^preriodic_task_list/', include([
        url(r'^delete_entity/', PeriodicTaskDeleteView.as_view(), name='preriodic_task_delete'),
        url(r'^(?P<pk>\d+)/preriodic_task_edit/', PeriodicTaskUpdateView.as_view(),
            name='interval_schedule_edit'),
        url(r'^preriodic_task_add/', PeriodicTaskCreateView.as_view(), name='preriodic_task_add'),
        url(r'^$', PeriodicTaskView.as_view(), name='preriodic_task_list'),
    ])),
    url(r'^crontab_schedule_list/', include([
        url(r'^delete_entity/', CrontabScheduleDeleteView.as_view(), name='crontab_schedule_delete'),
        url(r'^(?P<pk>\d+)/crontab_schedule_edit/', CrontabScheduleUpdateView.as_view(),
            name='interval_schedule_edit'),
        url(r'^crontab_schedule_add/', CrontabScheduleCreateView.as_view(), name='crontab_schedule_add'),
        url(r'^$', CrontabScheduleView.as_view(), name='crontab_schedule_list'),
    ])),
    url(r'^task_state_list/', include([
        url(r'^delete_entity/', TaskStateDeleteView.as_view(), name='task_state_delete'),
        url(r'^(?P<pk>\d+)/task_state_edit/', TaskStateUpdateView.as_view(),
            name='interval_schedule_edit'),
        url(r'^task_state_add/', TaskStateCreateView.as_view(), name='task_state_add'),
        url(r'^$', TaskStateView.as_view(), name='task_state_list'),
    ])),
]
