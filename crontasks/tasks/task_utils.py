import os
import re
import traceback
from uuid import uuid1

import logging
import requests
import yaml
from celery import task


import shlex

from cmdb.models import Host
from saltops2.settings import DEFAULT_LOGGER, PACKAGE_PATH, SALT_REST_URL
from saltrest.salt_https_api import salt_api_token
from saltrest.salt_token_id import token_id

logger = logging.getLogger(DEFAULT_LOGGER)


def getScriptType(types):
    if types == 0:
        return 'sls'
    elif types == 1:
        return 'sh'
    else:
        return 'sls'


def generateDynamicScript(
        script_content: str,
        script_type: str,
        param: str = "",
        extra_param: str = "",
        extend_dict: dict = None):
    """
    动态生成脚本文件
    :param script_content: 脚本内容
    :param script_type: 脚本类型，用于拼接文件名的后缀
    :param param: yaml格式的参数，用于替换动态参数
    :param extra_param: 扩展参数，yaml格式的参数，用于替换动态参数
    :param extend_dict:字典类型的扩展参数，用于替换动态参数
    :return: 脚本文件的名称，脚本的完整路径
    """
    logger.info("动态生成脚本文件")

    script_content = script_content.replace('\r', '')

    logger.info("填写动态变量")

    # 动态参数用${key}这样的结构存放,提取出所有的动态参数
    params = re.findall('\${(.*)}', script_content)
    if param != "" and params != "":
        yaml_params = yaml.load(param)
        for cmd_param in params:
            if ':' in cmd_param:
                script_content = script_content.replace('${%s}' % cmd_param,
                                                        yaml_params.get(cmd_param.split(":")[1]))

    if extra_param is not None and extra_param != "":
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
    # if SALT_OPS_CONFIG['connect_type'] == 'http':
    #     try:
    #         logger.info("当前执行模式为分离模式，发送脚本到Master节点")
    #         url = SALT_OPS_CONFIG['simple_service_url'] + '/upload'
    #         files = {'file': open(script_path, 'rb')}
    #         requests.post(url, files=files)
    #         logger.info("发送远程文件结束")
    #         return True
    #     except Exception as  e:
    #         logger.error(e)
    #         return False
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
            result = salt_api_token({'fun': 'state.sls', 'tgt': host.host if host.enable_ssh else host,
                                     'arg': filename},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(
                client=client)['return'][0]
            logger.info("执行结果为:%s", result)
        else:
            result = salt_api_token({'fun': 'cmd.script', 'tgt': host.host if host.enable_ssh else host,
                                     'arg': 'salt://%s.%s' % (filename, script_type)},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(
                client=client)['return'][0]
            logger.info("执行结果为:%s", result)
    else:
        if func_args is not None:
            # lex = shlex.shlex(func_args.strip())
            # lex.quotes = '"'
            # lex.whitespace_split = True
            # b = list(lex)
            # l = []
            # for i in b:
            #     s = i.replace('"', '')
            #     l.append(s)
            result = salt_api_token({'fun': func, 'tgt': host.host if host.enable_ssh else host,
                                     'arg': func_args},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(
                client=client)['return']
        else:
            result = salt_api_token({'fun': func, 'tgt': host.host if host.enable_ssh else host},
                                    SALT_REST_URL, {'X-Auth-Token': token_id()}).CmdRun(
                client=client)['return']

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


def get_host_client_type(enable_ssh: bool):
    if enable_ssh:
        return 'ssh'
    else:
        return 'local'