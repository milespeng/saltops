from rest_framework import serializers

from deploy_manager.admin import cmdThread
from deploy_manager.models import *


class ProjectVersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectVersion
        fields = ('name', 'project', 'files', 'is_default')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name',)


class DeployJobSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        obj = DeployJob.objects.create(**validated_data)
        thread = cmdThread(obj)
        thread.start()
        return obj

    class Meta:
        model = DeployJob
        fields = ('project_version', 'job_name')
