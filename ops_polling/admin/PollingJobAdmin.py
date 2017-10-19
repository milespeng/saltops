import logging

from django.contrib import admin
from django.forms import Textarea
from import_export.admin import ImportExportModelAdmin
from suit.admin import SortableTabularInline

from crontasks.tasks import generateDynamicScript, prepareScript, runSaltCommand, getHostViaResult
from ops_polling.models import PollingJob, PollingScript, models
from saltops2.settings import DEFAULT_LOGGER


class PollingScript(SortableTabularInline):
    model = PollingScript
    sortable = 'order'
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 1,
                   'cols': 40, })
        }
    }


@admin.register(PollingJob)
class PollingJobAdmin(ImportExportModelAdmin):
    def walk_job_action(self, request, queryset):

        logger = logging.getLogger(DEFAULT_LOGGER)

        for obj in queryset:
            pollingscript_list = obj.pollingscript_set.all()
            for host in obj.polling_hosts.all():
                for script in pollingscript_list:
                    logger.info("开始执行命令")
                    result = runSaltCommand(host, 4, '', 'cmd.run', script.tool_script)
                    targetHost, dataResult = getHostViaResult(result, host, host.host_name)
                    print(dataResult)
        self.message_user(request, "%s 个巡检任务被成功执行." % len(queryset))

    walk_job_action.short_description = "执行巡检"

    list_display = ['name', 'create_time', 'update_time']
    search_fields = ['name']
    inlines = (PollingScript,)
    actions = (walk_job_action,)
