from django.core.checks import Error, register

from saltops.settings import *


@register()
def saltops_check(app_configs, **kwargs):
    errors = []
    if SALT_OPS_CONFIG['connect_type'] != '' and SALT_OPS_CONFIG['simple_service_url'] == '':
        errors.append(
            Error(
                'SimpleService配置未正确设置',
                hint='使用分离部署请配置SimpleService的地址.',
                obj=[SALT_OPS_CONFIG['connect_type'], SALT_OPS_CONFIG['simple_service_url']],
                id='SaltOps.001',
            )
        )
    if SALT_OPS_CONFIG['package_path'] == '':
        errors.append(
            Error(
                '未配置SaltStack的SLS脚本路径',
                hint='使用分离部署请配置SimpleService的地址.SaltMaster的sls路径一致',
                id='SaltOps.002',
            )
        )
    if SALT_OPS_CONFIG['salt_api_url'] == '':
        errors.append(
            Error(
                '未配置SaltAPI的URL路径',
                hint='请安装SaltAPI并配置SaltAPI的URL路径',
                id='SaltOps.003',
            )
        )
    if SALT_OPS_CONFIG['salt_api_user'] == '':
        errors.append(
            Error(
                '未配置SaltAPI所使用的用户名',
                hint='未配置SaltAPI所使用的用户名',
                id='SaltOps.003',
            )
        )
    if SALT_OPS_CONFIG['salt_api_password'] == '':
        errors.append(
            Error(
                '未配置SaltAPI所使用的密码',
                hint='未配置SaltAPI所使用的密码',
                id='SaltOps.004',
            )
        )
    return errors
