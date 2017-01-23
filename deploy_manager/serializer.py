from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from deploy_manager.models import Project

#
# class ProjectSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Project
#         fields = ('name', 'host', 'project_module')
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
