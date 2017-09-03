from django.db import models
from common.models import BaseModel
from common.storages import OverwriteStorage
from deploy_manager.models.Project import Project, JOB_SCRIPT_TYPE
from django.core.validators import FileExtensionValidator

from saltops.settings import SALT_OPS_CONFIG


class ProjectVersion(BaseModel):
    project = models.ForeignKey(Project, default="", verbose_name="业务名称", blank=True, null=True, )
    files = models.FileField(verbose_name='SLS包', blank=True, null=True,
                             upload_to=SALT_OPS_CONFIG['package_path'],
                             validators=[FileExtensionValidator(['zip'])])
    software_files = models.FileField(verbose_name='应用包', blank=True, null=True,
                                      upload_to=SALT_OPS_CONFIG['package_path'])

    def __str__(self):
        return self.project.__str__() + '---' + self.files

    class Meta:
        verbose_name = "版本信息"
        verbose_name_plural = verbose_name
