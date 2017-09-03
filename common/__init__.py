from time import timezone

from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

# 注册自己为一个自定义的Tag
from django import template

register_lib = template.Library()


@register.filter
def join_queryset_attr(queryset, attr, delimiter=', '):
    """
    把结果集的属性用分隔符进行连接
    :param queryset: 结果集
    :param attr: 属性名
    :param delimiter: 分隔符
    :return: 
    """
    return delimiter.join([getattr(obj, attr, '') for obj in queryset])


@register.filter()
def str_to_int(value):
    """
    转换value为数值类型
    :param value: 
    :return: 
    """
    if value is not None and value != "":
        return int(value)
    else:
        return value


@register.filter
def pagination_range(total_page, current_num=1, display=5):
    """返回分页基础信息

    :param total_page: Total numbers of paginator
    :param current_num: current display page num
    :param display: Display as many as [:display:] page

    In order to display many page num on web like:
    < 1 2 3 4 5 >
    """
    try:
        current_num = int(current_num)
    except ValueError:
        current_num = 1

    start = current_num - display / 2 if current_num > display / 2 else 1
    end = start + display if start + display <= total_page else total_page + 1

    return range(int(start), int(end))


@register.filter()
def file_path_filter(value):
    if type(value) is str:
        return ''
    else:
        return value.name.split('/')[-1].split('.')[0]


@register.filter()
def bool_to_human(value):
    """
    转换布尔类型为中文
    :param value: 
    :return: 
    """
    if value is True:
        return '是'
    else:
        return '否'


@register.filter()
def replace_to_br(value: str):
    """
    将换行符转为html到换行符
    :param value: 
    :return: 
    """
    if value is not None:
        return mark_safe(value.replace('\\n', '<br/>'))
    else:
        return ''


@register.filter
def join_attr(seq, attr=None, sep=None):
    """
    将属性用分割符连接
    :param seq: 
    :param attr: 
    :param sep: 
    :return: 
    """
    if sep is None:
        sep = ', '
    if attr is not None:
        seq = [getattr(obj, attr) for obj in seq]
    return sep.join(seq)


@register.filter
def int_to_str(value):
    """
    转换数值为字符串
    :param value: 
    :return: 
    """
    return str(value)


@register.filter
def ts_to_date(ts):
    """
    时间戳转日期
    :param ts: 
    :return: 
    """
    try:
        ts = float(ts)
    except TypeError:
        ts = 0
    dt = timezone.datetime.fromtimestamp(ts). \
        replace(tzinfo=timezone.get_current_timezone())
    return dt.strftime('%Y-%m-%d %H:%M:%S')
