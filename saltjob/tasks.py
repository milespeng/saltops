import os
import traceback
from uuid import uuid1

import logging
import requests
import yaml
from celery import task

from cmdb.models import Host, HostIP
from deploy_manager.models import DeployJobDetail
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltops.settings import SALT_REST_URL, PACKAGE_PATH, SALT_CONN_TYPE, SALT_HTTP_URL, DEFAULT_LOGGER


@task(name='deployTask')
def deployTask(deployJob):
    logger = logging.getLogger(DEFAULT_LOGGER)

    logger.info("动态生成脚本文件")
    project = deployJob.project_version.project
    defaultVersion = project.projectversion_set.get(is_default=True)

    hosts = project.host.all()

    uid = uuid1().__str__()
    logger.info("脚本UUID为:%s", uid)

    isSubScript = defaultVersion.sub_job_script_type == 100

    scriptType = 0  # 默认为SLS

    if isSubScript is True:
        if project.job_script_type == 0:
            logger.info("脚本类型为sls")
            scriptPath = PACKAGE_PATH + uid + ".sls"
        if project.job_script_type == 1:
            logger.info("脚本类型为sh")
            scriptPath = PACKAGE_PATH + uid + ".sh"
            scriptType = 1
    else:
        if defaultVersion.sub_job_script_type == 0:
            logger.info("脚本类型为sls")
            scriptPath = PACKAGE_PATH + uid + ".sls"
        if defaultVersion.sub_job_script_type == 1:
            logger.info("脚本类型为sh")
            scriptPath = PACKAGE_PATH + uid + ".sh"
            scriptType = 1

    output = open(scriptPath, 'w')

    logger.info("填写动态变量")

    if isSubScript is True:
        playbookContent = project.playbook
    else:
        playbookContent = defaultVersion.subplaybook

    logger.info("处理扩展参数")

    if project.extra_param != "":
        extraparam = yaml.load(project.extra_param)[0]
        for key in extraparam:
            playbookContent = playbookContent.replace('${%s}' % key, extraparam[key])

    if defaultVersion.extra_param != '':
        extraparam = yaml.load(defaultVersion.extra_param)[0]
        for key in extraparam:
            playbookContent = playbookContent.replace('${%s}' % key, extraparam[key])

    playbookContent = playbookContent.replace('${version}', project.name)

    output.write(playbookContent)
    output.close()

    if SALT_CONN_TYPE == 'http':
        logger.info("当前执行模式为分离模式，发送脚本到Master节点")
        url = SALT_HTTP_URL + '/upload'
        files = {'file': open(scriptPath, 'rb')}
        requests.post(url, files=files)

    jobList = []

    for target in hosts:
        logger.info("执行脚本，目标主机为:%s", target)
        hasErr = False

        # SLS模式
        if scriptType == 0:

            if target.enable_ssh is False:
                result = salt_api_token({'fun': 'state.sls', 'tgt': target,
                                         'arg': uid},
                                        SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
            else:
                ins = salt_api_token({'fun': 'state.sls', 'tgt': target.host,
                                      'arg': uid},
                                     SALT_REST_URL, {'X-Auth-Token': token_id()})
                result = ins.sshRun()['return'][0]
            for master in result:
                if isinstance(result[master], dict):
                    if target.enable_ssh is False:
                        dataResult = result[master]
                        targetHost = Host.objects.get(host_name=master)
                    else:
                        dataResult = result[master]['return']
                        targetHost = Host.objects.get(host=master)
                    for cmd in dataResult:

                        if not dataResult[cmd]['result']:
                            hasErr = True

                        msg = ""
                        if "stdout" in dataResult[cmd]['changes']:
                            msg = dataResult[cmd]['changes']["stdout"]
                        stderr = ""
                        if "stderr" in dataResult[cmd]['changes']:
                            stderr = dataResult[cmd]['changes']["stderr"]

                        jobCmd = ""
                        if 'name' in dataResult[cmd]:
                            jobCmd = dataResult[cmd]['name']

                        duration = 0
                        if 'duration' in dataResult[cmd]:
                            duration = dataResult[cmd]['duration']

                        # startTime = None
                        # if 'start_time' in dataResult[cmd]:
                        #     startTime = dataResult[cmd]['start_time']
                        deployJobDetail = DeployJobDetail(
                            host=targetHost,
                            deploy_message=msg,
                            job=deployJob,
                            stderr=stderr,
                            job_cmd=jobCmd,
                            comment=dataResult[cmd]['comment'],
                            is_success=dataResult[cmd]['result'],
                            # start_time=startTime,
                            duration=duration,
                        )
                        jobList.append(deployJobDetail)

        if scriptType == 1:
            if target.enable_ssh is False:
                result = salt_api_token({'fun': 'cmd.script', 'tgt': target,
                                         'arg': 'salt://%s.sh' % uid},
                                        SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
            else:
                ins = salt_api_token({'fun': 'cmd.script', 'tgt': target.host,
                                      'arg': 'salt://%s.sh' % uid},
                                     SALT_REST_URL, {'X-Auth-Token': token_id()})
                result = ins.sshRun()['return'][0]
            for master in result:
                if target.enable_ssh is False:
                    dataResult = result[master]
                    targetHost = Host.objects.get(host_name=master)
                else:
                    dataResult = result[master]['return']
                    targetHost = Host.objects.get(host=master)
                if dataResult['stderr'] != '':
                    hasErr = True

                deployJobDetail = DeployJobDetail(
                    host=targetHost,
                    deploy_message=dataResult['stdout'],
                    job=deployJob,
                    stderr=dataResult['stderr'],
                    job_cmd=playbookContent,
                    is_success=True if dataResult['stderr'] == '' else False,
                )
                jobList.append(deployJobDetail)

    os.remove(scriptPath)
    deployJob.deploy_status = 1 if hasErr is False else 2
    deployJob.save()
    for i in jobList:
        i.save()
    logger.info("执行脚本完成")


@task(name='scanHostJob')
def scanHostJob():
    logger = logging.getLogger(DEFAULT_LOGGER)
    logger.info("开始执行主机扫描操作")

    logger.info('扫描主机状态列表')

    manageInstance = salt_api_token({'fun': 'manage.status'},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()})
    statusResult = manageInstance.runnerRun()
    upList = statusResult['return'][0]['up']
    # downList = statusResult['return'][0]['down']

    result = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                            SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]

    logger.info("扫描主机数量为[%s]", len(result))

    for host in result:
        try:
            rs = Host.objects.filter(host_name=host, host=result[host]["host"])
            if len(rs) == 0:
                logger.info("新增主机:%s", result[host]["host"])
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
                              mem_total=int(result[host]["mem_total"]),
                              minion_status=1 if host in upList else 0
                              )
                device.save()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=device)
                    hostip.save()
            else:
                entity = rs[0]
                logger.info("更新主机:%s", entity)
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
                entity.minion_status = 1 if host in upList else 0
                entity.save()

                HostIP.objects.filter(host=entity).delete()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=entity)
                    hostip.save()

        except Exception as e:
            logger.error("自动扫描出现异常:%s", e)

    sshResult = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                               SALT_REST_URL, {'X-Auth-Token': token_id()}).sshRun()['return'][0]
    logger.info("扫描主机数量为[%s]", len(sshResult))
    for host in sshResult:
        try:
            if 'return' in sshResult[host]:
                rs = Host.objects.filter(host=host)
                entity = rs[0]
                logger.info("更新主机:%s", host)
                entity.host_name = sshResult[host]['return']['fqdn'] if 'fqdn' in sshResult[host]['return'] else ""
                entity.kernel = sshResult[host]['return']['kernel']
                entity.kernel_release = sshResult[host]['return']['kernelrelease']
                entity.virtual = sshResult[host]['return']['virtual']
                entity.osrelease = sshResult[host]['return']['osrelease']
                entity.saltversion = sshResult[host]['return']['saltversion']
                entity.osfinger = sshResult[host]['return']['osfinger']
                entity.os_family = sshResult[host]['return']['os_family']
                entity.num_gpus = sshResult[host]['return']['num_gpus']
                entity.system_serialnumber = sshResult[host]['return']["serialnumber"]
                entity.cpu_model = sshResult[host]['return']["cpu_model"]
                entity.productname = sshResult[host]['return']["productname"]
                entity.osarch = sshResult[host]['return']["osarch"]
                entity.cpuarch = sshResult[host]['return']["cpuarch"]
                entity.os = sshResult[host]['return']["os"]
                # entity.num_cpus = int(sshResult[host]['return']["num_cpus"]),
                # entity.mem_total = int(sshResult[host]['return']["mem_total"]),
                entity.minion_status = 1
                entity.save()
                HostIP.objects.filter(host=entity).delete()
                for ip in sshResult[host]['return']["ipv4"]:
                    hostip = HostIP(ip=ip, host=entity)
                hostip.save()

        except Exception as e:
            traceback.print_exc()
