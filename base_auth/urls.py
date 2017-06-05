from django.conf.urls import include, url

from base_auth.views import *

urlpatterns = [

    url(r'^groups_list/', include([
        url(r'^delete_entity/', GroupDeleteView.as_view(), name='group_delete'),
        url(r'^(?P<pk>\d+)/group_edit/', GroupUpdateView.as_view(), name='group_edit'),
        url(r'^group_add/', GroupCreateView.as_view(), name='group_add'),
        url(r'^$', GroupView.as_view(), name='group_list'),
    ])),

]
