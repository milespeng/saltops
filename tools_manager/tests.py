from django.test import TestCase

from cmdb.models import Host
from saltjob.tasks import execTools
from tools_manager.models import *

TARGET_HOST = "ubuntu"


class ApacheModuleTest(TestCase):
    def setUp(self):
        try:
            tool_type = ToolsTypes.objects.create(name='测试模块')
            ToolsScript.objects.create(name='demo', tool_script='apache.version', tools_type=tool_type, tool_run_type=4)
            Host.objects.create(host_name=TARGET_HOST)
        except Exception as e:
            print(e)

    def test_apache_version(self):
        obj = ToolsScript.objects.get(name='demo')
        host = Host.objects.get(host_name=TARGET_HOST)
        list = []
        list.append(host.id)
        execTools(obj, list, "")
