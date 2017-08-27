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
from saltops.settings import DEFAULT_LOGGER, SALT_OPS_CONFIG
from tools_manager.models import ToolsExecDetailHistory, ToolsExecJob

import shlex

logger = logging.getLogger(DEFAULT_LOGGER)


def deploy_job_task(project_host_name: str,
                    project_version_name: str,
                    client_type: str):
    """
    此函数仅负责部署单个业务
    部署业务，部署业务约定以版本名称作为state名称，如部署golang，
    则版本名称为golang1_8_3，压缩包中，此文件夹的名称也需要为golang1_8_3，
    部署的时候，以salt [目标主机] state.apply [版本名称]
    :param project_host_name: 目标主机
    :param project_version_name: 版本名称
    :param client_type: 使用的客户端类型，minion则为local，ssh则为ssh
    :return:部署是否成功,单台主机部署结果列表
    """
    logger.info("执行部署，目标主机为:%s", project_host_name)
    result = salt_api_token({'fun': 'state.apply',
                             'tgt': project_host_name,
                             'arg': project_version_name},
                            SALT_OPS_CONFIG['salt_api_url'], {'X-Auth-Token': token_id()}).CmdRun(client=client_type)['return'][0]
    logger.info("执行结果为:%s", result)

    # 全生命周期是否部署成功
    deploy_success = True

    # SaltAPI执行完成后会返回很多的信息，仅提取需要的部分
    if client_type == 'local':
        data_result = result[project_host_name]
    else:
        data_result = result[project_host_name]['return']
    result_list = []
    for cmd in data_result:
        result_dict = {
            'msg': '',
            'stderr': '',
            'job_cmd': '',
            'duration': 0,
            'comment': '',
            'is_success': True,
        }
        if "stdout" in data_result[cmd]['changes']:
            result_dict['msg'] = data_result[cmd]['changes']["stdout"]
        if "stderr" in data_result[cmd]['changes']:
            result_dict['stderr'] = data_result[cmd]['changes']["stderr"]
            result_dict['is_success'] = False
            deploy_success = False;

        result_dict['job_cmd'] = cmd

        if 'duration' in data_result[cmd]:
            result_dict['duration'] = data_result[cmd]['duration']
        if 'comment' in data_result[cmd]:
            result_dict['comment'] = data_result[cmd]['comment']
        result_list.append(result_dict)
    return deploy_success, result_list
