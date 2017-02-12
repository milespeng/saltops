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

logger = logging.getLogger(DEFAULT_LOGGER)


@task(name='deployTask')
def deployTask(deployJob):
    logger.info("动态生成脚本文件")
    project = deployJob.project_version.project
    defaultVersion = project.projectversion_set.get(is_default=True)
    logger.info("使用的默认版本为%s", defaultVersion)

    hosts = project.host.all()
    logger.info("获取目标主机信息,目标部署主机共%s台", len(hosts))

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

    playbookContent = playbookContent.replace('${version}', defaultVersion.name)

    output.write(playbookContent)
    output.close()
    logger.info("写入文件结束，文件为%s", scriptPath)

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
                logger.info("使用Minion方式执行")
                result = salt_api_token({'fun': 'state.sls', 'tgt': target,
                                         'arg': uid},
                                        SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
                logger.info("执行结果为%s", result)
            else:
                logger.info("使用SaltSSH方式执行")
                ins = salt_api_token({'fun': 'state.sls', 'tgt': target.host,
                                      'arg': uid},
                                     SALT_REST_URL, {'X-Auth-Token': token_id()})
                result = ins.sshRun()['return'][0]
                logger.info("执行结果为%s", result)

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
                logger.info("使用Minion方式执行")
                result = salt_api_token({'fun': 'cmd.script', 'tgt': target,
                                         'arg': 'salt://%s.sh' % uid},
                                        SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
                logger.info("执行结果为%s", result)

            else:
                logger.info("使用SaltSSH方式执行")
                ins = salt_api_token({'fun': 'cmd.script', 'tgt': target.host,
                                      'arg': 'salt://%s.sh' % uid},
                                     SALT_REST_URL, {'X-Auth-Token': token_id()})
                result = ins.sshRun()['return'][0]
                logger.info("执行结果为%s", result)
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
    logger.info('扫描Minion启动状态列表')
    upList = []
    try:
        manageInstance = salt_api_token({'fun': 'manage.status'},
                                        SALT_REST_URL, {'X-Auth-Token': token_id()})
        statusResult = manageInstance.runnerRun()
        upList = statusResult['return'][0]['up']
    except Exception as e:
        logger.info("没有任何主机启动状态信息:%s" % e)

    logger.info("扫描客户端注册列表")
    minionsInstance = salt_api_token({'fun': 'key.list_all'},
                                     SALT_REST_URL, {'X-Auth-Token': token_id()})
    minionList = minionsInstance.wheelRun()['return'][0]['data']['return']
    minions_pre = minionList['minions_pre']
    logger.info("待接受主机:%s" % len(minions_pre))
    # minions = minionList['minions']
    minions_rejected = minionList['minions_rejected']
    logger.info("已拒绝主机:%s", len(minions_rejected))

    minions_denied = minionList['minions_denied']
    logger.info("已禁用主机:%s", len(minions_denied))

    # logger.info("自动主机")
    # for minion in minions_pre:
    #     logger.info("自动接受主机:%s" % minion)
    #     salt_api_token({'fun': 'key.accept', 'match': minion},
    #                    SALT_REST_URL, {'X-Auth-Token': token_id()}).wheelRun()
        # rs = Host.objects.filter(host_name=minion)
        # if len(rs) == 0:
        #     try:
        #         device = Host(host_name=minion, minion_status=2)
        #         device.save()
        #     except Exception as e:
        #         logger.info(e)

    logger.info("获取Minion主机资产信息")
    result = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                            SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
    logger.info("扫描Minion数量为[%s]", len(result))

    for host in result:
        try:
            minionstatus = 0
            if host in upList:
                minionstatus = 1
            if host in minions_rejected:
                minionstatus = 3
            if host in minions_denied:
                minionstatus = 4

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
                              num_gpus=result[host]["num_gpus"],
                              system_serialnumber=result[host]["system_serialnumber"]
                              if 'system_serialnumber' in result[host] else result[host]["serialnumber"],
                              cpu_model=result[host]["cpu_model"],
                              productname=result[host]["productname"],
                              osarch=result[host]["osarch"],
                              cpuarch=result[host]["osarch"],
                              os=result[host]["os"],
                              # num_cpus=int(result[host]["num_cpus"]),
                              mem_total=result[host]["mem_total"],
                              minion_status=minionstatus
                              )
                device.save()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=device)
                    hostip.save()
            else:
                entity = rs[0]
                logger.info("更新主机:%s", entity)
                entity.kernel = result[host]["kernel"]
                # entity.num_cpus = result[host]["num_cpus"],
                entity.kernel_release = result[host]["kernelrelease"]
                entity.virtual = result[host]["virtual"]
                entity.osrelease = result[host]["osrelease"],
                entity.saltversion = result[host]["saltversion"]
                entity.osfinger = result[host]["osfinger"]
                entity.os_family = result[host]["os_family"]
                entity.num_gpus = result[host]["num_gpus"]
                entity.system_serialnumber = result[host]["system_serialnumber"] \
                    if 'system_serialnumber' in result[host] else result[host]["serialnumber"]
                entity.cpu_model = result[host]["cpu_model"]
                entity.productname = result[host]["productname"]
                entity.osarch = result[host]["osarch"]
                entity.cpuarch = result[host]["osarch"]
                entity.os = result[host]["os"]
                entity.mem_total = result[host]["mem_total"]
                entity.minion_status = minionstatus
                entity.save()

                HostIP.objects.filter(host=entity).delete()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=entity)
                    hostip.save()

        except Exception as e:
            logger.error("自动扫描出现异常:%s", e)

    logger.info("扫描Salt-SSH主机信息")
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
