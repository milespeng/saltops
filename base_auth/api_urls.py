from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as drf_views

from base_auth.viewsets.user import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^v1/user/', include([
        url(r'^login', csrf_exempt(drf_views.obtain_auth_token), name='api.login'),
    ])),
]
