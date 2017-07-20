import os
import re
import traceback
from uuid import uuid1

import logging
import requests
import yaml
from celery import task
from post_office import mail

from cmdb.models import Host, HostIP, HostGroup
from deploy_manager.models import *
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltops.settings import SALT_REST_URL, PACKAGE_PATH, SALT_CONN_TYPE, SALT_HTTP_URL, DEFAULT_LOGGER
from tools_manager.models import ToolsExecDetailHistory, ToolsExecJob

import shlex

logger = logging.getLogger(DEFAULT_LOGGER)


def generateDynamicScript(script_content, script_type, param="", extra_param="", extend_dict=None):
    """
    动态生成脚本文件
    :return: 脚本文件的名称，脚本的完整路径
    """
    logger.info("动态生成脚本文件")

    script_content = script_content.replace('\r', '')

    logger.info("填写动态变量")

    params = re.findall('\${(.*)}', script_content)
    if param != "" and params != "":
        yaml_params = yaml.load(param)
        for cmd_param in params:
            if ':' in cmd_param:
                script_content = script_content.replace('${%s}' % cmd_param, yaml_params.get(cmd_param.split(":")[1]))

    if extra_param != "":
        yaml_params = yaml.load(extra_param)
        for cmd_param in yaml_params:
            script_content = script_content.replace('${%s}' % cmd_param, yaml_params.get(cmd_param))

    if extend_dict is not None:
        for k in extend_dict:
            script_content = script_content.replace('${%s}' % k, extend_dict[k])

    uid = uuid1().__str__()
    scriptPath = PACKAGE_PATH + uid + '.' + script_type
    output = open(scriptPath, 'wb')
    output.write(bytes(script_content, encoding='utf8'))
    output.close()
    logger.info("写入文件结束，文件为%s", scriptPath)
    return uid, scriptPath


def prepareScript(script_path):
    """
    判断执行模式，执行对应的操作
    :return:
    """
    if SALT_CONN_TYPE == 'http':
        try:
            logger.info("当前执行模式为分离模式，发送脚本到Master节点")
            url = SALT_HTTP_URL + '/upload'
            files = {'file': open(script_path, 'rb')}
            requests.post(url, files=files)
            logger.info("发送远程文件结束")
            return True
        except Exception as  e:
            logger.error(e)
            return False
    return True


def runSaltCommand(host, script_type, filename, func=None, func_args=None):
    """
    执行远程命令
    :param host:
    :param script_type:
    :param filename:
    :return:
    """
    client = 'local'
    if host.enable_ssh is True:
        client = 'ssh'
    if func is None:
        if script_type == 'sls':
            result = salt_api_token({'fun': 'state.sls', 'tgt': host,
                                     'arg': filename},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(client=client)['return'][0]
            logger.info("执行结果为:%s", result)
        else:
            result = salt_api_token({'fun': 'cmd.script', 'tgt': host,
                                     'arg': 'salt://%s.%s' % (filename, script_type)},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(client=client)['return'][0]
            logger.info("执行结果为:%s", result)
    else:
        if func_args is not None:
            lex = shlex.shlex(func_args.strip())
            lex.quotes = '"'
            lex.whitespace_split = True
            b = list(lex)
            l = []
            for i in b:
                s = i.replace('"', '')
                l.append(s)
            result = salt_api_token({'fun': func, 'tgt': host,
                                     'arg': tuple(l)},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(client=client)['return']
        else:
            result = salt_api_token({'fun': func, 'tgt': host},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(client=client)['return']

        logger.info("执行结果为:%s", result)
    if isinstance(result, dict):
        return result
    else:
        return result[0]


def getHostViaResult(result, host, hostname):
    """
    因为Salt-SSH和Salt-Minion获取结果的方式不太一样，所以要区别对待
    :param result:
    :param host:
    :param hostname:
    :return:
    """
    if host.enable_ssh is False:
        dataResult = result[hostname]
        targetHost = Host.objects.get(host_name=hostname)
    else:
        dataResult = result[hostname]['return']
        targetHost = Host.objects.get(host=hostname)
    return targetHost, dataResult


@task(name='execTools')
def execTools(obj, hostList, ymlParam):
    """
    执行工具
    :param obj:  工具实体
    :param hostList: 主机ID列表
    :param ymlParam: yml格式的参数
    :return: ToolsExecJob
    """

    # 新增执行记录
    hostSet = Host.objects.filter(pk__in=hostList).all()
    toolExecJob = ToolsExecJob(
        param=ymlParam,
        tools=obj
    )
    toolExecJob.save()
    toolExecJob.hosts.add(*hostSet)
    toolExecJob.save()

    # Salt命令模块名
    func = None
    # Salt命令参数
    func_args = None

    func = "cmd.script"
    script_type = 'sls'
    if obj.tool_run_type == 1:
        script_type = "sh"
    if obj.tool_run_type == 2:
        script_type = "ps1"
    if obj.tool_run_type == 3:
        script_type = "py"
    if obj.tool_run_type == 5:
        script_type = "bat"
    if obj.tool_run_type == 4:
        # 命令格式为cmd.run xxx xxx
        func = obj.tool_script.split(' ')[0]
        func_args = obj.tool_script[len(func):]

        # 提取需要替换的参数内容，参数为${xxxx:xxxx}
        params = re.findall('\${(.+?)}', func_args)
        if params != "":
            yaml_param = yaml.load(ymlParam)
            for cmd_param in params:
                func_args = func_args.replace('${%s}' % cmd_param, yaml_param.get(cmd_param.split(":")[1]))

    script_name = ""
    script_path = ""
    prepare_script_result = True
    # 非Salt命令，需要把脚本送到Master的BasePath里面
    if obj.tool_run_type != 4:
        script_name, script_path = generateDynamicScript(obj.tool_script, script_type, ymlParam, "", None)
        prepare_script_result = prepareScript(script_path)

    logger.info("开始执行命令")
    logger.info("获取目标主机信息,目标部署主机共%s台", hostSet.count())
    exec_detail_list = []
    for target in hostSet:
        try:
            if prepare_script_result is False:
                errmsg = "执行失败：发送文件到远端服务器失败，请检查SimpleService是否启动成功"
                execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                    host=target,
                                                    exec_result='执行失败',
                                                    err_msg=errmsg)
                execDetail.save()
                exec_detail_list.append(execDetail)
                continue

            if obj.tool_run_type == 1:
                func_args = 'salt://%s.sh' % script_name

            elif obj.tool_run_type == 3:
                func_args = 'salt://%s.py' % script_name

            elif obj.tool_run_type == 2:
                func_args = 'salt://%s.ps' % script_name

            elif obj.tool_run_type == 5:
                func_args = 'salt://%s.bat' % script_name

            elif obj.tool_run_type == 0:
                func = 'state.sls'
                func_args = script_name

            result = runSaltCommand(target, script_type, script_name, func, func_args)

            if len(result) == 0:
                execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                    host=target,
                                                    exec_result='无返回结果，请检查Minion是否连通',
                                                    err_msg='')
                execDetail.save()
                exec_detail_list.append(execDetail)
            for master in result:
                targetHost, dataResult = getHostViaResult(result, target, master)

                if obj.tool_run_type == 0:
                    for cmd in dataResult:
                        if 'comment' in dataResult[cmd]:
                            rs_msg = dataResult[cmd]['comment']
                        if 'data' in dataResult[cmd]:
                            for key in dataResult[cmd]['data']:
                                rs_msg = rs_msg + '\n' + key + ':' + str(dataResult[cmd]['data'][key])
                        execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                            host=targetHost,
                                                            exec_result=rs_msg,
                                                            err_msg='')
                        execDetail.save()
                        exec_detail_list.append(execDetail)
                elif obj.tool_run_type == 4:
                    rs_msg = ""
                    rs_msg += targetHost.host_name + '\n--------\n'
                    if dataResult is None:
                        rs_msg = '执行完成'
                    # Salt-API返回的结果一会是list一会是dict。。
                    elif isinstance(dataResult, list):
                        for k in dataResult:
                            if isinstance(k, dict):
                                for v in k:
                                    rs_msg += ("\n" + v + ":" + str(k[v]))
                            else:
                                rs_msg += "\n".join(k)
                    elif isinstance(dataResult, str):
                        rs_msg = dataResult
                    # elif isinstance(dataResult,dict):
                    #     for k in dataResult:
                    #
                    elif isinstance(dataResult, bool):
                        rs_msg = str(dataResult)

                    elif 'columns' in dataResult:  # 针对MySQL返回的结果做特别的处理
                        rs_msg += "<table class='table table-striped table-bordered table-hover " \
                                  " dataTables-example dataTable'><tr>"
                        for c in dataResult['columns']:
                            rs_msg += "<th>%s</th>" % str(c)
                        rs_msg += "</tr>"
                        for c in dataResult['results']:
                            rs_msg += "<tr>"
                            for o in c:
                                rs_msg += "<td>%s</td>" % str(o)
                            rs_msg += "</tr>"
                        # TODO: 还有个query_time可以显示
                        rs_msg += "</table>"
                        rs_msg += '\n'
                    else:
                        for cmd in dataResult:
                            rs_msg = rs_msg + '\n' + cmd + ':' + str(dataResult[cmd])
                            rs_msg += '\n'

                    execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                        host=targetHost,
                                                        exec_result=rs_msg,
                                                        err_msg='')
                    execDetail.save()
                    exec_detail_list.append(execDetail)
                elif obj.tool_run_type == 1 or obj.tool_run_type == 3:
                    execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                        host=targetHost,
                                                        exec_result=dataResult,
                                                        err_msg='')
                    execDetail.save()
                    exec_detail_list.append(execDetail)
                else:
                    execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                        host=targetHost,
                                                        exec_result=dataResult['stdout'],
                                                        err_msg=dataResult['stderr'])
                    execDetail.save()
                    exec_detail_list.append(execDetail)
        except Exception as e:
            print(e)
            errmsg = "执行失败"
            if isinstance(dataResult, str):
                errmsg = dataResult

            execDetail = ToolsExecDetailHistory(tool_exec_history=toolExecJob,
                                                host=target,
                                                exec_result='执行失败',
                                                err_msg=errmsg)
            execDetail.save()
            exec_detail_list.append(execDetail)

    return toolExecJob, exec_detail_list


def getScriptType(types):
    if types == 0:
        return 'sls'
    elif types == 1:
        return 'sh'
    else:
        return 'sls'


@task(name='deployTask')
def deployTask(deploy_job: DeployJob,
               operation: int,
               target_hosts=[]):
    """
    部署业务
    :param uninstall:
    :param uninstall_host:
    :param deployJob:
    :return:
    """
    try:
        project = deploy_job.project_version.project
        default_version = deploy_job.project_version
        logger.info("使用的默认版本为%s", default_version)

        # 判断是否使用版本的部署脚本
        script_type = 'sls'
        playbookContent = ''
        # 0 安装  1 卸载 2 状态守护 3 启动 4 停止 5 状态获取
        if operation == 0:
            if default_version.install_script != '':
                playbookContent = default_version.install_script
                script_type = getScriptType(default_version.install_job_script_type)
            else:
                playbookContent = project.install_script
                script_type = getScriptType(project.install_job_script_type)
        if operation == 1:
            if default_version.anti_install_script != '':
                playbookContent = default_version.anti_install_script
                script_type = getScriptType(default_version.anti_install_script_type)
            else:
                playbookContent = project.anti_install_script
                script_type = getScriptType(project.anti_install_script_type)
        if operation == 2:
            if default_version.stateguard_script != '':
                playbookContent = default_version.stateguard_script
                script_type = getScriptType(default_version.stateguard_script_type)
            else:
                playbookContent = project.stateguard_script
                script_type = getScriptType(project.stateguard_script_type)
        if operation == 3:
            if default_version.start_script != '':
                playbookContent = default_version.start_script
                script_type = getScriptType(default_version.start_script_type)
            else:
                playbookContent = project.start_scriptw
                script_type = getScriptType(project.start_script_type)
        if operation == 4:
            if default_version.stop_script != '':
                playbookContent = default_version.stop_script
                script_type = getScriptType(default_version.stop_script_type)
            else:
                playbookContent = project.stop_script
                script_type = getScriptType(project.stop_script_type)
        if operation == 5:
            if default_version.state_script != '':
                playbookContent = default_version.state_script
                script_type = getScriptType(default_version.state_script_type)
            else:
                playbookContent = project.state_script
                script_type = getScriptType(project.state_script_type)

        extent_dict = (
            {'version': default_version.name}
        )
        if default_version.extra_param != '':
            extra_params = default_version.extra_param
        else:
            extra_params = project.extra_param

        script_name, script_path = generateDynamicScript(playbookContent, script_type, project.extra_param,
                                                         extra_params, extent_dict)
        prepare_result = prepareScript(script_path)
        if prepare_result is False:
            deploy_job.deploy_status = 2
            deploy_job.save()
            logger.info("执行失败，请检查SimpleService是否启动")
            return

        jobList = []
        hosts = []
        if len(target_hosts) == 0:
            project_hosts = ProjectHost.objects.filter(project=project)
            for o in project_hosts:
                hosts.append(o.host)
            project_host_groups = ProjectHostGroup.objects.filter(project=project)
            for o in project_host_groups:
                host = Host.objects.filter(host_group=o.hostgroup)
                for h in host:
                    hosts.append(h)
            hosts = list(set(hosts))
        else:
            hosts = target_hosts

        logger.info("获取目标主机信息,目标部署主机共%s台", len(hosts))
        hasErr = False
        for target in hosts:

            logger.info("执行脚本，目标主机为:%s", target)

            result = runSaltCommand(target, script_type, script_name)

            # SLS模式
            if script_type == 'sls':
                for master in result:
                    if isinstance(result[master], dict):
                        targetHost, dataResult = getHostViaResult(result, target, master)
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
                                job=deploy_job,
                                stderr=stderr,
                                job_cmd=jobCmd,
                                comment=dataResult[cmd]['comment'],
                                is_success=dataResult[cmd]['result'],
                                # start_time=startTime,
                                duration=duration,
                            )
                            jobList.append(deployJobDetail)

            else:
                for master in result:
                    targetHost, dataResult = getHostViaResult(result, target, master)
                    if dataResult['stderr'] != '':
                        hasErr = True

                    deployJobDetail = DeployJobDetail(
                        host=targetHost,
                        deploy_message=dataResult['stdout'],
                        job=deploy_job,
                        stderr=dataResult['stderr'],
                        job_cmd=playbookContent,
                        is_success=True if dataResult['stderr'] == '' else False,
                    )
                    jobList.append(deployJobDetail)

        os.remove(script_path)
        deploy_job.deploy_status = 1 if hasErr is False else 2
        deploy_job.save()
        for i in jobList:
            i.save()
        logger.info("执行脚本完成")
        return deploy_job
    except Exception as e:
        deploy_job.deploy_status = 2
        deploy_job.save()
        logger.info("执行失败%s:" % e)

        mail.send(
            '529280602@qq.com',  # List of email addresses also accepted
            subject='My email',
            message='Hi there!',
            html_message='Hi <strong>there</strong>!',
        )
        return deploy_job


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
    minions_rejected = []
    minions_denied = []
    minions_pre = []
    try:
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
    except Exception as e:
        logger.info("扫描主机键值状态异常:%s" % e)
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

                    oldip_list = [i.ip for i in HostIP.objects.filter(host=entity)]
                    for ip in set(result[host]["ipv4"]) - set(oldip_list):
                        hostip = HostIP(ip=ip, host=entity)
                        hostip.save()
                    for ip in set(oldip_list) - set(result[host]["ipv4"]):
                        HostIP.objects.filter(ip=ip).delete()

        except Exception as e:
            traceback.print_exc()


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
                           SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun()

            for host in obj.host.all():
                if SALT_CONN_TYPE == 'http':
                    url = SALT_HTTP_URL + '/read'
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


@task(name='scanProjectConfig')
def scanProjectConfig():
    project_config_file = ProjectConfigFile.objects.all()
    for project in project_config_file:
        loadProjectConfig(project.project.id)


@task(name='scanProjectState')
def scanProjectState():
    """
    状态采集
    :return:
    """
    project_host_lists = ProjectHost.objects.all()
    project_host_group_list = ProjectHostGroup.objects.all()
    logger.info("共扫描业务%s个" % len(project_host_lists))
    hostlist = []
    for o in project_host_group_list:
        Host.objects.filter(host_group=o)
        hostlist.append(o)
    for k in project_host_lists:
        version = ProjectVersion.objects.get(pk=int(k.project.current_version_id))
        job = DeployJob(project_version=version, job_name='采集业务' + k.host.host_name + ":" + version.name)
        job.save()
        hostlist.append(k.host)
        logger.info("扫描业务%s" % version.project.name)
        deployjob = deployTask.delay(job, 5, hostlist)
        deployjob_obj = DeployJobDetail.objects.get(job=deployjob.result)
        if deployjob_obj.deploy_message != '':
            k.is_running = True
            logger.info("业务%s运行中" % version.project.name)
        else:
            k.is_running = False
            logger.info("业务%s未运行" % version.project.name)
        k.save()


@task(name='scanProjectGuard')
def scanProjectGuard():
    """
    状态采集
    :return:
    """
    project_host_lists = ProjectHost.objects.all()
    project_host_group_list = ProjectHostGroup.objects.all()
    logger.info("共扫描业务%s个" % len(project_host_lists))
    hostlist = []
    for o in project_host_group_list:
        Host.objects.filter(host_group=o)
        hostlist.append(o)
    for k in project_host_lists:
        version = ProjectVersion.objects.get(pk=int(k.project.current_version_id))
        job = DeployJob(project_version=version, job_name='守护' + k.host.host_name + ":" + version.name)
        job.save()
        hostlist.append(k.host)
        logger.info("扫描业务%s" % version.project.name)
        deployjob = deployTask.delay(job, 2, hostlist)
