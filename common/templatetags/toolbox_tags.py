import datetime
from django import template

register = template.Library()


@register.inclusion_tag("common/tags/toolbox_select_filter_dynamic.html")
def toolbox_select_filter_dynamic(select_name, select_value, select_label, select_datasource):
    """
    工具栏的搜索按钮
    :return:
    """
    return {
        'select_name': select_name,
        'select_value': select_value,
        'select_label': select_label,
        'select_datasource': select_datasource
    }


@register.inclusion_tag("common/tags/toolbox_text_filter.html")
def toolbox_text_filter(txt_widget_name, placeholder, name):
    """
    工具栏的搜索按钮
    :return:
    """
    return {
        'txt_widget_name': txt_widget_name,
        'placeholder': placeholder,
        'name': name
    }


@register.inclusion_tag("common/tags/toolbox_search.html")
def toolbox_search():
    """
    工具栏的搜索按钮
    :return: 
    """
    return {
    }


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
