from django.conf.urls import url
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from cmdb.models import Host, HostIP
from crontasks.tasks import scan_host_job


class IPInline(admin.TabularInline):
    model = HostIP
    fields = ['ip', 'ip_type']
    verbose_name = "IP"
    verbose_name_plural = "IP"
    extra = 0


@admin.register(Host)
class HostAdmin(ImportExportModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^scan_host/$',
                self.admin_site.admin_view(self.scan_host),
                name='scan_host',
            ),
        ]
        return custom_urls + urls

    change_list_template = 'cmdb_host_list.html'
    list_display = ['host_name', 'kernel',
                    'host', 'rack', 'system_serialnumber',
                    'os', 'virtual', 'enable_ssh', 'minion_status', 'create_time', 'update_time']
    search_fields = ['host']
    list_filter = ['virtual', 'os_family', 'os', 'rack', 'minion_status']
    inlines = [IPInline]

    def scan_host(self, request):
        scan_host_job()
        self.message_user(request, "主机扫描完成")
        return super(HostAdmin, self).changelist_view(request=request)

    def save_formset(self, request, form, formset, change):
        entity = form.save()
        formset.save()
        # 如果主机是SSH类型的，把SSH列表更新一遍
        if entity.enable_ssh is True:
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

                with open('/etc/salt/roster', 'w') as content:
                    content.write(rosterString)
