import logging
import requests
import xlrd
from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltops.settings import PER_PAGE, SALT_HTTP_URL, DEFAULT_LOGGER
from saltops.settings_backup import SALT_CONN_TYPE


class AssertImportCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'cmdb/assert_import_index.html'


class AssertImportView(LoginRequiredMixin, JSONResponseMixin,
                       AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        logger = logging.getLogger(DEFAULT_LOGGER)

        assert_file = request.FILES.get("file", None)
        wb = xlrd.open_workbook(filename=None, file_contents=assert_file.read())
        # 读取机房等级信息
        idc_level_table = wb.sheets()[0]
        for i in range(1, idc_level_table.nrows):
            row = idc_level_table.row_values(i)
            if len(IDCLevel.objects.filter(name=row[0])) == 0:
                IDCLevel(name=row[0], comment=row[1]).save()

        # 读取ISP信息
        isp_table = wb.sheets()[1]
        for i in range(1, isp_table.nrows):
            row = isp_table.row_values(i)
            if len(ISP.objects.filter(name=row[0])) == 0:
                ISP(name=row[0]).save()

        # 读取机房信息
        idc_table = wb.sheets()[2]
        for i in range(1, idc_table.nrows):
            row = idc_table.row_values(i)
            if len(IDC.objects.filter(name=row[0])) == 0:
                try:
                    IDC(name=row[0], bandwidth=row[1],
                        phone=row[2], linkman=row[3],
                        address=row[4], concat_email=row[5],
                        network=row[6], operator=ISP.objects.get(name=row[7]),
                        type=IDCLevel.objects.get(name=row[8]), comment=row[9]).save()
                except Exception as e:
                    pass

        # 机柜
        for i in range(1, wb.sheets()[3].nrows):
            row = wb.sheets()[3].row_values(i)
            if len(Cabinet.objects.filter(name=row[1])) == 0:
                try:
                    Cabinet(idc=IDC.objects.get(name=row[0]), name=row[1]).save()
                except Exception as e:
                    pass

        # 机架
        for i in range(1, wb.sheets()[4].nrows):
            row = wb.sheets()[4].row_values(i)
            if len(Rack.objects.filter(name=row[1])) == 0:
                try:
                    Rack(idc=IDC.objects.get(name=row[0]),
                         cabinet=Cabinet.objects.get(name=row[1]),
                         name=row[2]).save()
                except Exception as e:
                    pass

        # 主机组
        for i in range(1, wb.sheets()[5].nrows):
            row = wb.sheets()[5].row_values(i)
            if len(HostGroup.objects.filter(name=row[1])) != 0:
                continue
            try:
                if row[0] == "":
                    HostGroup(name=row[1]).save()
                else:
                    HostGroup(parent=HostGroup.objects.get(name=row[0]), name=row[1]).save()
            except Exception as e:
                pass

        # 主机
        for i in range(1, wb.sheets()[6].nrows):
            row = wb.sheets()[6].row_values(i)
            try:
                enable_sudo = False
                if row[7] != '0':
                    enable_sudo = True
            except Exception as e:
                pass
            if len(Host.objects.filter(host_name=row[1])) != 0:
                continue
            if row[1] != '' and Host.objects.filter(host=row[1]).count() == 0:
                try:
                    host = Host(
                        host_name=row[1],
                        host=row[2],
                        enable_ssh=True,
                        ssh_username=row[5],
                        ssh_password=row[6],
                        enable_sudo=enable_sudo)
                    if str(row[0]) != '' and HostGroup.objects.filter(name=str(row[0])).count() != 0:
                        host.host_group = HostGroup.objects.get(name=str(row[0]))
                    if str(row[3]) != '' and IDC.objects.filter(name=str(row[3])).count() != 0:
                        host.idc = IDC.objects.get(name=str(row[3]))
                    if str(row[4]) != '' and Cabinet.objects.filter(name=str(row[4])).count() != 0:
                        host.cabinet = Cabinet.objects.get(name=str(row[4]))
                    if str(row[5]) != '' and Rack.objects.filter(name=str(row[5])).count() != 0:
                        host.rack = Rack.objects.get(name=str(row[5]))
                    host.save()

                except Exception as e:
                    print('导入主机失败', e)

            # 更新一遍Rouster信息
            hosts = Host.objects.all()

            rosterString = ""
            for host in hosts:
                if host.enable_ssh is True:
                    rosterString += """

                %s:
                    host: %s
                    user: %s
                    passwd: %s
                    sudo: %s
                    tty: True

                                """ % (host.host, host.host, host.ssh_username, host.ssh_password,
                                       host.enable_ssh)

            if SALT_CONN_TYPE == 'http':
                requests.post(SALT_HTTP_URL + '/rouster', data={'content': rosterString})
            else:
                try:
                    with open('/etc/salt/roster', 'w') as content:
                        content.write(rosterString)
                except Exception as e:
                    logger.error("写入SaltSSH文件失败，无权限或无该文件")
        return self.render_json_response({})
