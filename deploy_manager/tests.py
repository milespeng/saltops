import json
import logging

import os
import zipfile

from django.test import TestCase
from saltjob.tasks import deploy_job_task
import socket

from saltops.settings import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)


class DeployJobTestCase(TestCase):
    def setUp(self):
        self.hostname = socket.gethostname()
        logger.info("主机名：%s" % self.hostname)
        if not os.path.exists('./static/scripts/golang1_8_3'):
            logger.info('未找到测试部署包，解压测试部署包')
            f = zipfile.ZipFile('./doc/sls/golang1_8_3.zip', 'r')
            for file in f.namelist():
                f.extract(file, './static/scripts')
            f.close()

    def test_minion_single_deploy(self):
        is_success, result = deploy_job_task(self.hostname, 'golang1_8_3', 'local', 0)
        print('Is Deploy Success:%s' % is_success)
        print('Deploy Result:%s' % json.dumps(result, indent=4, sort_keys=True))

        is_success, result = deploy_job_task(self.hostname, 'golang1_8_3', 'local', 1)
        print('Is Deploy Success:%s' % is_success)
        print('Deploy Result:%s' % json.dumps(result, indent=4, sort_keys=True))

        is_success, result = deploy_job_task(self.hostname, 'golang1_8_3', 'local', 2)
        print('Is Deploy Success:%s' % is_success)
        print('Deploy Result:%s' % json.dumps(result, indent=4, sort_keys=True))

        is_success, result = deploy_job_task(self.hostname, 'golang1_8_3', 'local', 3)
        print('Is Deploy Success:%s' % is_success)
        print('Deploy Result:%s' % json.dumps(result, indent=4, sort_keys=True))
