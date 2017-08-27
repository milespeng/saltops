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
from saltjob.tasks import *
from saltops.settings import SALT_REST_URL, PACKAGE_PATH, SALT_CONN_TYPE, SALT_HTTP_URL, DEFAULT_LOGGER
from tools_manager.models import ToolsExecDetailHistory, ToolsExecJob

import shlex

logger = logging.getLogger(DEFAULT_LOGGER)


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
        logger.info("开始部署任务")

        project = deploy_job.project_version.project
        logger.info("部署目标业务为[%s]" % project)

        default_version = deploy_job.project_version
        logger.info("使用的默认版本为%s", default_version)

        # 判断是否使用版本内的部署脚本
        script_type = 'sls'
        playbookContent = ''
        # 0 安装  1 卸载 2 状态守护 3 启动 4 停止 5 状态获取
        if operation == 0:
            if default_version.install_script is not None and default_version.install_script != '':
                playbookContent = default_version.install_script
                script_type = getScriptType(default_version.install_job_script_type)
                logger.info("业务安装操作，使用版本内的部署脚本")
            else:
                playbookContent = project.install_script
                script_type = getScriptType(project.install_job_script_type)
                logger.info("业务安装操作，使用业务的部署脚本")
        if operation == 1:
            if default_version.anti_install_script is not None and default_version.anti_install_script != '':
                playbookContent = default_version.anti_install_script
                script_type = getScriptType(default_version.anti_install_script_type)
                logger.info("业务卸载操作，使用版本内的卸载脚本")
            else:
                playbookContent = project.anti_install_script
                script_type = getScriptType(project.anti_install_script_type)
                logger.info("业务卸载操作，使用业务的卸载脚本")
        if operation == 2:
            if default_version.stateguard_script is not None and default_version.stateguard_script != '':
                playbookContent = default_version.stateguard_script
                script_type = getScriptType(default_version.stateguard_script_type)
                logger.info("业务守护操作，使用版本内的守护脚本")
            else:
                playbookContent = project.stateguard_script
                script_type = getScriptType(project.stateguard_script_type)
                logger.info("业务守护操作，使用业务的守护脚本")
        if operation == 3:
            if default_version.start_script is not None and default_version.start_script != '':
                playbookContent = default_version.start_script
                script_type = getScriptType(default_version.start_script_type)
                logger.info("业务启动操作，使用版本内的启动脚本")
            else:
                playbookContent = project.start_script
                script_type = getScriptType(project.start_script_type)
                logger.info("业务启动操作，使用业务的启动脚本")
        if operation == 4:
            if default_version.stop_script is not None and default_version.stop_script != '':
                playbookContent = default_version.stop_script
                script_type = getScriptType(default_version.stop_script_type)
                logger.info("业务停止操作，使用版本内的停止脚本")
            else:
                playbookContent = project.stop_script
                script_type = getScriptType(project.stop_script_type)
                logger.info("业务停止操作，使用业务的停止脚本")
        if operation == 5:
            if default_version.state_script != '':
                playbookContent = default_version.state_script
                script_type = getScriptType(default_version.state_script_type)
                logger.info("业务状态采集操作，使用版本内的状态采集脚本")
            else:
                playbookContent = project.state_script
                script_type = getScriptType(project.state_script_type)
                logger.info("业务状态采集操作，使用业务的状态采集脚本")
        extent_dict = (
            {'version': default_version.name}
        )
        logger.info("内置参数[%s]" % extent_dict)

        if default_version.extra_param != '':
            extra_params = default_version.extra_param
        else:
            extra_params = project.extra_param

        logger.info("扩展参数[%s]" % extra_params)

        script_name, script_path = generateDynamicScript(playbookContent, script_type, project.extra_param,
                                                         extra_params, extent_dict)
        prepare_result = prepareScript(script_path)
        if prepare_result is False:
            deploy_job.deploy_status = 2
            deploy_job.save()
            logger.error("执行失败，请检查SimpleService是否启动")
            return

        jobList = []
        hosts = []

        # TODO:逻辑有些奇怪，目标主机怎么会为空呢？
        if len(target_hosts) == 0:
            project_hosts = ProjectHost.objects.filter(project=project)
            for o in project_hosts:
                hosts.append(o.host)
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
        logger.info("执行失败%s:" % traceback.format_exc())

        mail.send(
            '529280602@qq.com',  # List of email addresses also accepted
            subject='My email',
            message='Hi there!',
            html_message='Hi <strong>there</strong>!',
        )
        return deploy_job
