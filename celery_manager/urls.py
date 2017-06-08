from django.conf.urls import include, url

from celery_manager.views import *

urlpatterns = [
    url(r'^interval_schedule_list/', include([
        url(r'^delete_entity/', IntervalScheduleDeleteView.as_view(), name='interval_schedule_delete'),
        url(r'^(?P<pk>\d+)/interval_schedule_edit/', IntervalScheduleUpdateView.as_view(), name='interval_schedule_edit'),
        url(r'^interval_schedule_add/', IntervalScheduleCreateView.as_view(), name='interval_schedule_add'),
        url(r'^$', IntervalScheduleView.as_view(), name='interval_schedule_list'),
    ])),



]
