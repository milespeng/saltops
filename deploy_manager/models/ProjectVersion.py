from django.db import models
from common.models import BaseModel
from deploy_manager.models.Project import Project, JOB_SCRIPT_TYPE
from saltops.settings import PACKAGE_PATH


class ProjectVersion(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="版本名称")
    project = models.ForeignKey(Project, default="", verbose_name="业务名称", blank=True, null=True, )
    files = models.FileField(verbose_name='版本', blank=True, null=True, upload_to=PACKAGE_PATH)
    install_job_script_type = models.IntegerField(default=0, choices=JOB_SCRIPT_TYPE,
                                                  verbose_name='部署脚本类型')

    install_script = models.TextField(verbose_name='部署脚本', null=True, blank=True,
                                      help_text='${version}代表默认版本号')

    anti_install_script_type = models.IntegerField(default=0, choices=JOB_SCRIPT_TYPE,
                                                   verbose_name='卸载部署脚本类型')
    anti_install_script = models.TextField(verbose_name='卸载脚本', null=True, blank=True,
                                           help_text='${version}代表默认版本号')

    stateguard_script_type = models.IntegerField(default=0, choices=JOB_SCRIPT_TYPE,
                                                 verbose_name='守护脚本类型')
    stateguard_script = models.TextField(verbose_name='守护脚本', null=True, blank=True,
                                         help_text='${version}代表默认版本号')

    start_script_type = models.IntegerField(default=0, choices=JOB_SCRIPT_TYPE,
                                            verbose_name='启动脚本类型')
    start_script = models.TextField(verbose_name='启动脚本', null=True, blank=True,
                                    help_text='${version}代表默认版本号')

    stop_script_type = models.IntegerField(default=0, choices=JOB_SCRIPT_TYPE,
                                           verbose_name='停止脚本类型')
    stop_script = models.TextField(verbose_name='停止脚本', null=True, blank=True,
                                   help_text='${version}代表默认版本号')

    state_script_type = models.IntegerField(default=0, choices=JOB_SCRIPT_TYPE,
                                            verbose_name='状态脚本类型')
    state_script = models.TextField(verbose_name='状态脚本', null=True, blank=True,
                                    help_text='${version}代表默认版本号')

    extra_param = models.TextField(verbose_name='扩展参数', default="", blank=True, null=True)
    anti_install_playbook = models.TextField(verbose_name='卸载脚本', null=True, blank=True,
                                             help_text='${version}代表默认版本号')

    def __str__(self):
        return self.project.__str__() + '---' + self.name

    class Meta:
        verbose_name = "版本信息"
        verbose_name_plural = verbose_name
