from django.test import TestCase

from cmdb.models import Host
from saltjob.tasks import execTools
from tools_manager.models import *

TARGET_HOST = "e8e39f7d599c"


def execJob(script_name, ymlParam=""):
    obj = ToolsScript.objects.get(name=script_name)
    host = Host.objects.get(host_name=TARGET_HOST)
    list = []
    list.append(host.id)
    execTools(obj, list, ymlParam)


def init_tool(list):
    try:
        tool_type = ToolsTypes.objects.create(name='测试模块')
        for obj in list:
            ToolsScript.objects.create(name=obj['name'], tool_script=obj['tool_script'], tools_type=tool_type,
                                       tool_run_type=obj['tool_run_type'])
        Host.objects.create(host_name=TARGET_HOST)
    except Exception as e:
        print(e)


class ApacheModuleTest(TestCase):
    def setUp(self):
        init_tool(list=(
            {'tool_script': 'apache.version', 'name': 'demo', 'tool_run_type': 4}
        ))

    def test_apache_version(self):
        execJob('demo')


class ShellModuleTest(TestCase):
    def setUp(self):
        init_tool(list=(
            {'tool_script': 'ps -ef', 'name': 'script_ps', 'tool_run_type': 2},
            {'tool_script': 'ps -ef|grep ${进程名称:thread_name}', 'name': 'script_ps_args', 'tool_run_type': 2},
        ))

    def test_script_ps(self):
        """
        测试执行简单命令
        :return:
        """
        execJob('script_ps')

    def test_script_ps_with_args(self):
        """
        测试执行带参数命令
        :return:
        """
        execJob('script_ps_args', "{thread_name: salt}")
