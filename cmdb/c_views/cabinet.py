from django.forms import inlineformset_factory

from cmdb.models import Cabinet
from cmdb.models import IDC
from cmdb.models import ISP


def idc_list_plugin():
    idc = IDC.objects.all()
    return {'idc': idc}
