from django.core.checks import Error, register

from saltops.settings import *


@register()
def example_check(app_configs, **kwargs):
    errors = []
    if SALT_CONN_TYPE != '' and SALT_HTTP_URL == '':
        errors.append(
            Error(
                'SimpleService配置未正确设置',
                hint='使用分离部署请配置SimpleService的地址.',
                obj=[SALT_CONN_TYPE, SALT_HTTP_URL],
                id='SaltOps.001',
            )
        )
    if PACKAGE_PATH == '':
        errors.append(
            Error(
                '未配置SaltStack的SLS脚本路径',
                hint='使用分离部署请配置SimpleService的地址.SaltMaster的sls路径一致',
                id='SaltOps.002',
            )
        )
    if SALT_REST_URL == '':
        errors.append(
            Error(
                '未配置SaltAPI的URL路径',
                hint='请安装SaltAPI并配置SaltAPI的URL路径',
                id='SaltOps.003',
            )
        )
    if SALT_USER == '':
        errors.append(
            Error(
                '未配置SaltAPI所使用的用户名',
                hint='未配置SaltAPI所使用的用户名',
                id='SaltOps.003',
            )
        )
    if SALT_PASSWORD == '':
        errors.append(
            Error(
                '未配置SaltAPI所使用的密码',
                hint='未配置SaltAPI所使用的密码',
                id='SaltOps.004',
            )
        )
    return errors
