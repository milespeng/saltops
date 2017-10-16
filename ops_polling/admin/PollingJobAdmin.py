from django.contrib import admin
from django.forms import Textarea
from import_export.admin import ImportExportModelAdmin
from suit.admin import SortableTabularInline

from ops_polling.models import PollingJob, PollingScript, models


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
        #TODO: 循环执行脚本，生成报告，任务写到Job里面去
        pass

    walk_job_action.short_description = "执行巡检"

    list_display = ['name', 'create_time', 'update_time']
    search_fields = ['name']
    inlines = (PollingScript,)
    actions = (walk_job_action,)
