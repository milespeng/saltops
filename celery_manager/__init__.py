from django.template.defaultfilters import register
from django.utils.safestring import mark_safe


@register.filter()
def interval_to_str(value):
    """
    转换value为数值类型
    :param value: 
    :return: 
    """
    if value == 'days':
        return '天'
    if value == 'hours':
        return '小时'
    if value == 'minutes':
        return '分'
    if value == 'seconds':
        return '秒'
    if value == 'microseconds':
        return '微秒'
