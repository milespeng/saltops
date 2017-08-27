import logging

import requests
from celery.task import task

from deploy_manager.models import *
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltops.settings import DEFAULT_LOGGER, SALT_OPS_CONFIG

logger = logging.getLogger(DEFAULT_LOGGER)

@task(name='scan_project_config')
def scan_project_config():
    project_config_file = ProjectConfigFile.objects.all()
    for project in project_config_file:
        loadProjectConfig(project.project.id)

def loadProjectConfig(id):
    obj = Project.objects.get(pk=id)
    targets = ""
    for host in obj.host.all():
        if host.enable_ssh is False:
            targets += host.host_name + ","
        else:
            targets += host.host + ","
    if targets != "":
        targets = targets[0:len(targets) - 1]
        for configobj in obj.projectconfigfile_set.all():
            salt_api_token({'fun': 'cp.push', 'tgt': targets, 'arg': configobj.config_path},
                           SALT_OPS_CONFIG['salt_api_url'], {'X-Auth-Token': token_id()}).CmdRun()

            for host in obj.host.all():
                if SALT_OPS_CONFIG['connect_type'] == 'http':
                    url = SALT_OPS_CONFIG['simple_service_url'] + '/read'
                    if host.enable_ssh is False:
                        data = requests.post(url, data={
                            "name": "/var/cache/salt/master/minions/" + host.host_name + '/files' + configobj.config_path}).content
                        data = str(data, encoding="utf-8")
                    else:
                        data = requests.post(url, data={
                            "name": "/var/cache/salt/master/minions/" + host.host + configobj.config_path}).content
                        data = str(data, encoding="utf-8")
                else:
                    data = open("/var/cache/salt/master/minions/" + host.host + configobj.config_path, 'r').read()

                project_host = ProjectHost.objects.get(project=obj, host=host)
                ProjectHostConfigFile.objects.filter(project_host=project_host).delete()
                entity = ProjectHostConfigFile(project_host=project_host, file_path=configobj.config_path,
                                               file_content=data)
                entity.save()





