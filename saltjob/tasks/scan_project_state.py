import logging

from celery.task import task

from deploy_manager.models import *
from saltops.settings import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)


@task(name='scanProjectState')
def scan_project_state():
    """
    状态采集
    :return:
    """
    project_host_lists = ProjectHost.objects.all()
    logger.info("共扫描业务%s个" % len(project_host_lists))
    hostlist = []
    for k in project_host_lists:
        version = ProjectVersion.objects.get(pk=int(k.project.current_version_id))
        job = DeployJob(project_version=version, job_name='采集业务' + k.host.host_name + ":" + version.name)
        job.save()
        hostlist.append(k.host)
        logger.info("扫描业务%s" % version.project.name)
        deployjob = deployTask.delay(job, 5, hostlist)
        deployjob_obj = DeployJobDetail.objects.get(job=deployjob.result)
        if deployjob_obj.deploy_message != '':
            k.is_running = True
            logger.info("业务%s运行中" % version.project.name)
        else:
            k.is_running = False
            logger.info("业务%s未运行" % version.project.name)
        k.save()
