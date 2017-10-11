import os
import re
import traceback
from uuid import uuid1

import logging
import requests
import yaml
from celery import task

import shlex

from cmdb.models import Host, HostIP
from saltops2.settings import DEFAULT_LOGGER, SALT_REST_URL
from saltrest.salt_https_api import salt_api_token
from saltrest.salt_token_id import token_id

logger = logging.getLogger(DEFAULT_LOGGER)

@task(name='scan_host_job')
def scan_host_job():
    """
    扫描客户端信息
    :return:
    """
    logger.info('扫描Minion启动状态列表')
    upList = []
    try:
        manageInstance = salt_api_token({'fun': 'manage.status'},
                                        SALT_REST_URL, {'X-Auth-Token': token_id()})
        statusResult = manageInstance.runnerRun()
        upList = statusResult['return'][0]['up']
        logger.debug("SaltMinion状态列表[%s]" % upList)
    except Exception as e:
        logger.error("没有任何主机启动状态信息:%s")
        logger.error(traceback.format_exc())

    logger.info("扫描客户端注册列表")
    minions_rejected = []
    minions_denied = []
    minions_pre = []
    try:
        minionsInstance = salt_api_token({'fun': 'key.list_all'},
                                         SALT_REST_URL, {'X-Auth-Token': token_id()})
        minionList = minionsInstance.wheelRun()['return'][0]['data']['return']
        minions_pre = minionList['minions_pre']

        logger.info("待接受主机:%s" % len(minions_pre))
        logger.debug("待接受主机[%s]" % minions_pre)

        minions_rejected = minionList['minions_rejected']
        logger.info("已拒绝主机:%s", len(minions_rejected))
        logger.debug("已拒绝主机[%s]", minions_rejected)

        minions_denied = minionList['minions_denied']
        logger.info("已禁用主机:%s", len(minions_denied))
        logger.debug("已禁用主机[%s]" % minions_denied)

    except Exception as e:
        logger.info("扫描主机键值状态异常:%s" % e)
        logger.error(traceback.format_exc())

    logger.info("获取Minion主机资产信息")
    result = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                            SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()['return'][0]
    logger.info("扫描Minion数量为[%s]", len(result))
    logger.debug("Minions资产信息[%s]" % result)

    Host.objects.update(minion_status=0)

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
                productname = ""
                if "productname" in result[host]:
                    productname = result[host]['productname']

                device = Host(host_name=host,
                              kernel=result[host]["kernel"] if 'kernel' in result[host] else "",
                              kernel_release=result[host]["kernelrelease"] if 'kernelrelease' in result[host] else "",
                              virtual=result[host]["virtual"] if 'virtual' in result[host] else "",
                              host=result[host]["host"] if 'host' in result[host] else "",
                              osrelease=result[host]["osrelease"] if 'osrelease' in result[host] else "",
                              saltversion=result[host]["saltversion"] if 'saltversion' in result[host] else "",
                              osfinger=result[host]["osfinger"] if 'osfinger' in result[host] else "",
                              os_family=result[host]["os_family"] if 'os_family' in result[host] else "",
                              num_gpus=result[host]["num_gpus"] if 'num_gpus' in result[host] else 0,
                              system_serialnumber=result[host]['serialnumber'] if 'serialnumber' in result[
                                  host] else "",
                              cpu_model=result[host]["cpu_model"] if 'cpu_model' in result[host] else "",
                              productname=result[host]['productname'] if "productname" in result[host]else"",
                              osarch=result[host]["osarch"] if 'osarch' in result[host] else "",
                              cpuarch=result[host]["cpuarch"] if 'cpuarch' in result[host] else "",
                              os=result[host]["os"] if 'os' in result[host] else "",
                              # num_cpus=int(result[host]["num_cpus"]),
                              mem_total=result[host]["mem_total"] if 'mem_total' in result[host] else 0,
                              minion_status=minionstatus
                              )
                device.save()
                for ip in result[host]["ipv4"]:
                    hostip = HostIP(ip=ip, host=device)
                    hostip.save()
            else:
                entity = rs[0]
                logger.info("更新主机:%s", entity)
                entity.kernel = result[host]["kernel"] if 'kernel' in result[host] else ""
                # entity.num_cpus = result[host]["num_cpus"],
                entity.kernel_release = result[host]["kernelrelease"] if 'kernelrelease' in result[host] else ""
                entity.virtual = result[host]["virtual"] if 'virtual' in result[host] else ""
                entity.osrelease = result[host]["osrelease"] if 'osrelease' in result[host] else "",
                entity.saltversion = result[host]["saltversion"] if 'saltversion' in result[host] else ""
                entity.osfinger = result[host]["osfinger"] if 'osfinger' in result[host] else ""
                entity.os_family = result[host]["os_family"] if 'os_family' in result[host] else ""
                entity.num_gpus = result[host]["num_gpus"] if 'num_gpus' in result[host] else 0
                entity.system_serialnumber = result[host]["serialnumber"] if 'serialnumber' in result[host] else ""
                entity.cpu_model = result[host]["cpu_model"] if 'cpu_model' in result[host] else ""
                entity.productname = result[host]["productname"] if 'productname' in result[host] else ""
                entity.osarch = result[host]["osarch"] if 'osarch' in result[host] else ""
                entity.cpuarch = result[host]["cpuarch"] if 'cpuarch' in result[host] else ""
                entity.os = result[host]["os"] if 'os' in result[host] else ""
                entity.mem_total = result[host]["mem_total"] if 'mem_total' in result[host] else 0
                entity.minion_status = minionstatus
                entity.save()

                oldip_list = [i.ip for i in HostIP.objects.filter(host=entity)]
                for ip in set(result[host]["ipv4"]) - set(oldip_list):
                    hostip = HostIP(ip=ip, host=entity)
                    hostip.save()
                for ip in set(oldip_list) - set(result[host]["ipv4"]):
                    HostIP.objects.filter(ip=ip).delete()

        except Exception as e:
            logger.error("自动扫描出现异常:%s", e)
            logger.error(traceback.format_exc())

    logger.info("扫描Salt-SSH主机信息")
    sshResult = salt_api_token({'fun': 'grains.items', 'tgt': '*'},
                               SALT_REST_URL, {'X-Auth-Token': token_id()}).sshRun()['return'][0]
    logger.info("扫描主机数量为[%s]", len(sshResult))
    for host in sshResult:
        try:
            if 'return' in sshResult[host]:
                rs = Host.objects.filter(host=host)
                if rs is not None:
                    entity = rs[0]
                    logger.info("更新主机:%s", host)

                    if 'fqdn' in sshResult[host]['return']:
                        entity.host_name = sshResult[host]['return']['fqdn']
                    else:
                        entity.host_name = ''

                    if 'kernel' in sshResult[host]['return']:
                        entity.kernel = sshResult[host]['return']['kernel']
                    else:
                        entity.kernel = ''

                    if 'kernelrelease' in sshResult[host]['return']:
                        entity.kernel_release = sshResult[host]['return']['kernelrelease']
                    else:
                        entity.kernel_release = ''

                    if 'virtual' in sshResult[host]['return']:
                        entity.virtual = sshResult[host]['return']['virtual']
                    else:
                        entity.virtual = ''

                    if 'osrelease' in sshResult[host]['return']:
                        entity.osrelease = sshResult[host]['return']['osrelease']
                    else:
                        entity.osrelease = ''

                    if 'saltversion' in sshResult[host]['return']:
                        entity.saltversion = sshResult[host]['return']['saltversion']
                    else:
                        entity.saltversion = ''

                    if 'osfinger' in sshResult[host]['return']:
                        entity.osfinger = sshResult[host]['return']['osfinger']
                    else:
                        entity.osfinger = ''

                    if 'os_family' in sshResult[host]['return']:
                        entity.os_family = sshResult[host]['return']['os_family']
                    else:
                        entity.os_family = ''

                    if 'num_gpus' in sshResult[host]:
                        entity.num_gpus = sshResult[host]['return']['num_gpus']
                    else:
                        entity.num_gpus = 0

                    if "serialnumber" in sshResult[host]:
                        entity.system_serialnumber = sshResult[host]['return']["serialnumber"]
                    else:
                        entity.system_serialnumber = ''

                    if "cpu_model" in sshResult[host]['return']:
                        entity.cpu_model = sshResult[host]['return']["cpu_model"]
                    else:
                        entity.cpu_model = ''

                    if "productname" in sshResult[host]['return']:
                        entity.productname = sshResult[host]['return']["productname"]
                    else:
                        entity.productname = ''

                    if "osarch" in sshResult[host]['return']:
                        entity.osarch = sshResult[host]['return']["osarch"]
                    else:
                        entity.osarch = ''

                    if "cpuarch" in sshResult[host]['return']:
                        entity.cpuarch = sshResult[host]['return']["cpuarch"]
                    else:
                        entity.cpuarch = ''

                    if "os" in sshResult[host]['return']:
                        entity.os = sshResult[host]['return']["os"]
                    else:
                        entity.os = ''
                    # entity.num_cpus = sshResult[host]['return']["num_cpus"],
                    # entity.mem_total = sshResult[host]['return']["mem_total"],
                    entity.minion_status = 1
                    entity.save()

                    oldip_list = [i.ip for i in HostIP.objects.filter(host=entity)]
                    for ip in set(sshResult[host]['return']["ipv4"]) - set(oldip_list):
                        hostip = HostIP(ip=ip, host=entity)
                        hostip.save()
                    for ip in set(oldip_list) - set(sshResult[host]['return']["ipv4"]):
                        HostIP.objects.filter(ip=ip).delete()

        except Exception as e:
            logger.error(traceback.format_exc())
