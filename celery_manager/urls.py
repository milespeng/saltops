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

]
