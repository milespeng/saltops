import os
from uuid import uuid1

import requests
from celery import task

from cmdb.models import Host, HostIP
from deploy_manager.models import DeployJobDetail
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltops.settings import SALT_REST_URL, PACKAGE_PATH, SALT_CONN_TYPE, SALT_HTTP_URL


@task(name='deployTask')
def deployTask(deployJob):
    # 动态生成SLS
    project = deployJob.project_version.project
    hosts = project.host.all()
    uid = uuid1().__str__()

    if project.job_script_type == 0:
        scriptPath = PACKAGE_PATH + uid + ".sls"
    if project.job_script_type == 1:
        scriptPath = PACKAGE_PATH + uid + ".sh"

    output = open(scriptPath, 'w')
    defaultVersion = project.projectversion_set.get(is_default=True)
    playbookContent = project.playbook.replace('${version}', defaultVersion.name)
    output.write(playbookContent)
    output.close()

    # 根据执行模式，判断是否发送文件到主节点
    if SALT_CONN_TYPE == 'http':
        url = SALT_HTTP_URL + '/upload'
        files = {'file': open(scriptPath, 'rb')}
        requests.post(url, files=files)

    jobList = []
    # 指定目标主机
    for target in hosts:
        result = None

        hasErr = False

        # SLS模式
        if project.job_script_type == 0:
            # 这里先用同步执行，发现异步执行好像也没什么区别的样子

            result = salt_api_token({'fun': 'state.sls', 'tgt': target,
                                     'arg': uid},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]

            for master in result:
                if isinstance(result[master], dict):
                    for cmd in result[master]:
                        # 判断总体任务是否失败，一个步骤失败则整个部署任务都失败
                        if not result[master][cmd]['result']:
                            hasErr = True

                        targetHost = Host.objects.get(host_name=master)
                        msg = ""
                        if "stdout" in result[master][cmd]['changes']:
                            msg = result[master][cmd]['changes']["stdout"]
                        stderr = ""
                        if "stderr" in result[master][cmd]['changes']:
                            stderr = result[master][cmd]['changes']["stderr"]

                        jobCmd = ""
                        if 'name' in result[master][cmd]:
                            jobCmd = result[master][cmd]['name']

                        duration = 0
                        if 'duration' in result[master][cmd]:
                            duration = result[master][cmd]['duration']

                        deployJobDetail = DeployJobDetail(
                            host=targetHost,
                            deploy_message=msg,
                            job=deployJob,
                            stderr=stderr,
                            job_cmd=jobCmd,
                            comment=result[master][cmd]['comment'],
                            is_success=result[master][cmd]['result'],
                            # start_time=result[master][cmd]['start_time'],
                            duration=duration,
                        )
                        jobList.append(deployJobDetail)

        # Script模式
        if project.job_script_type == 1:
            result = salt_api_token({'fun': 'cmd.script', 'tgt': target,
                                     'arg': 'salt://%s.sh' % uid},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
            for master in result:
                targetHost = Host.objects.get(host_name=master)
                if result[master]['stderr'] != '':
                    hasErr = True

                deployJobDetail = DeployJobDetail(
                    host=targetHost,
                    deploy_message=result[master]['stdout'],
                    job=deployJob,
                    stderr=result[master]['stderr'],
                    job_cmd=playbookContent,
                    is_success=True if result[master]['stderr'] == '' else False,
                )
                jobList.append(deployJobDetail)

    os.remove(scriptPath)
    deployJob.deploy_status = 1 if hasErr == False else 2
    deployJob.save()
    for i in jobList:
        i.save()


@task(name='scanHostJob')
def scanHostJob():
    print("开始作业")
    result = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                            SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
    print("作业调用结果")
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
