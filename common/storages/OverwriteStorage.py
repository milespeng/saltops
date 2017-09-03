from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from saltops.settings import SALT_OPS_CONFIG


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(SALT_OPS_CONFIG['package_path'], name))
        return name
