from django.forms import inlineformset_factory
import better_exceptions
from cmdb.models import Cabinet
from cmdb.models import IDC
from cmdb.models import ISP


def idc_list_plugin():
    isp_type = ISP.objects.all()
    return {'isp_type': isp_type}
