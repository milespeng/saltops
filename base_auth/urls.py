from django.conf.urls import include, url

from base_auth.views import *

urlpatterns = [

    url(r'^groups_list/', include([
        url(r'^delete_entity/', GroupDeleteView.as_view(), name='group_delete'),
        url(r'^(?P<pk>\d+)/group_edit/', GroupUpdateView.as_view(), name='group_edit'),
        url(r'^group_add/', GroupCreateView.as_view(), name='group_add'),
        url(r'^$', GroupView.as_view(), name='group_list'),
    ])),
    url(r'^user_list/', include([
        url(r'^delete_entity/', UserDeleteView.as_view(), name='user_delete'),
        url(r'^(?P<pk>\d+)/user_edit/', UserUpdateView.as_view(), name='user_edit'),
        url(r'^user_add/', UserCreateView.as_view(), name='user_add'),
        url(r'^$', UserView.as_view(), name='user_list'),
    ])),

]
