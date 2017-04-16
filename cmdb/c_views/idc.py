from cmdb.models import ISP


def idc_list_plugin():
    isp_type = ISP.objects.all()
    return {'isp_type': isp_type}
