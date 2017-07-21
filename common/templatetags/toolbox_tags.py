import datetime
from django import template

register = template.Library()


@register.inclusion_tag("common/tags/toolbox_add.html")
def toolbox_add(url):
    """
    工具栏的新增按钮
    :param url: 新增按钮跳转的URL
    :return: 
    """
    return {
        'url': url
    }


@register.inclusion_tag("common/tags/toolbox_batch_delete.html")
def toolbox_batch_delete():
    """
    工具栏的删除按钮
    :return: 
    """
    return {}
