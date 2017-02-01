import os
from uuid import uuid1

import salt.client
from celery import task

from cmdb.models import Host, HostIP
from deploy_manager.models import DeployJobDetail
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltops.settings import SALT_REST_URL, PACKAGE_PATH


@task(name='deployTask')
def deployTask(deployJob):
    project = deployJob.project_version.project
    hosts = project.host.all()
    uid = uuid1().__str__()
    scriptPath = PACKAGE_PATH + uid + ".sls"
    output = open(scriptPath, 'w')
    defaultVersion = project.projectversion_set.get(is_default=True)
    playbookContent = project.playbook.replace('${version}', defaultVersion.name)
    output.write(playbookContent)
    output.close()

    target = ""
    for host in hosts:
        target = host.host_name + ","
    if target != "":
        target = target[0:len(target) - 1]
    result = None

    if project.job_script_type == 0:
        result = salt_api_token({'fun': 'state.sls', 'tgt': target,
                                 'arg': uid},
                                SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
    if project.job_script_type == 1:
        # 脚本类型的下个版本再支持
        pass

    for master in result:
        if isinstance(result[master], dict):
            for cmd in result[master]:
                targetHost = Host.objects.get(host_name=master)
                msg = ""
                if "stdout" in result[master][cmd]['changes']:
                    msg = result[master][cmd]['changes']["stdout"]
                stderr = ""
                if "stderr" in result[master][cmd]['changes']:
                    stderr = result[master][cmd]['changes']["stderr"]
                deployJobDetail = DeployJobDetail(
                    host=targetHost,
                    deploy_message=msg,
                    job=deployJob,
                    stderr=stderr,
                    job_cmd=result[master][cmd]['name'],
                    # start_time=result[master][cmd]['start_time'],
                    duration=result[master][cmd]['duration'],
                )
                deployJobDetail.save()

    os.remove(scriptPath)
    deployJob.deploy_status = 1
    deployJob.save()


@task(name='scanHostJob')
def scanHostJob():
    result = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                            SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
    for host in result:
        try:
            rs = Host.objects.filter(host_name=host, host=result[host]["host"])
            if len(rs) == 0:
                device = Host(host_name=host,
                              kernel=result[host]["kernel"],
                              kernel_release=result[host]["kernelrelease"],
                              virtual=result[host]["virtual"],
                              host=result[host]["host"],
                              osrelease=result[host]["osrelease"],
                              saltversion=result[host]["saltversion"],
                              osfinger=result[host]["osfinger"],
                              os_family=result[host]["os_family"],
                              num_gpus=int(result[host]["num_gpus"]),
                              system_serialnumber=result[host]["system_serialnumber"]
                              if 'system_serialnumber' in result[host] else result[host]["serialnumber"],
                              cpu_model=result[host]["cpu_model"],
                              productname=result[host]["productname"],
                              osarch=result[host]["osarch"],
                              cpuarch=result[host]["osarch"],
                              os=result[host]["os"],
                              # num_cpus=int(result[host]["num_cpus"]),
                              mem_total=int(result[host]["mem_total"]), )
                device.save()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=device)
                    hostip.save()
            else:
                entity = rs[0]
                # str = result[host]["num_cpus"]
                entity.kernel = result[host]["kernel"]
                # entity.num_cpus = str,
                entity.kernel_release = result[host]["kernelrelease"]
                entity.virtual = result[host]["virtual"]
                entity.osrelease = result[host]["osrelease"],
                entity.saltversion = result[host]["saltversion"]
                entity.osfinger = result[host]["osfinger"]
                entity.os_family = result[host]["os_family"]
                entity.num_gpus = int(result[host]["num_gpus"])
                entity.system_serialnumber = result[host]["system_serialnumber"] \
                    if 'system_serialnumber' in result[host] else result[host]["serialnumber"]
                entity.cpu_model = result[host]["cpu_model"]
                entity.productname = result[host]["productname"]
                entity.osarch = result[host]["osarch"]
                entity.cpuarch = result[host]["osarch"]
                entity.os = result[host]["os"]
                entity.mem_total = int(result[host]["mem_total"])

                entity.save()

                HostIP.objects.filter(host=entity).delete()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=entity)
                    hostip.save()

        except Exception as e:
            print(e)
