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
from crontasks.tasks import prepareScript, runSaltCommand, getHostViaResult, generateDynamicScript
from ops_tools.models import ToolsExecJob, ToolsExecDetailHistory
from saltops2.settings import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)


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
                                                        exec_result=dataResult['stdout'],
                                                        err_msg=dataResult['stderr'])
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