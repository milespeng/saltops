from tools_manager.models import *
from tools_manager.models.ToolsScript import TOOL_RUN_TYPE
from collections import namedtuple


def tool_script_list_plugin():
    tools_types = ToolsTypes.objects.all()
    return {'tools_types': tools_types}


