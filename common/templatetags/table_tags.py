from django import template

register = template.Library()


@register.inclusion_tag("common/tags/table.html")
def table(id, edit_url, delete_id, *args):
    """
    简单表格
    :param id: 行记录的ID 
    :param edit_url: 编辑记录URL
    :param delete_id: 删除记录的ID
    :param args: 行记录，按照填写顺序进行展示
    :return: 
    """
    return {
        'datas': args,
        'delete_id': delete_id,
        'edit_url': edit_url,
        'id': id,
    }


@register.inclusion_tag("common/tags/table_head.html")
def table_head(config, order_by, ordering, operation_style='width:10%'):
    """
    表头
    :param config:表头配置，用@分割，表头名字@排序ID@表头样式 
    :param operation_style: 操作列的样式
    :return: 
    """
    headers = []
    for o in config.split(','):
        map_content = {}
        lists = o.split('@')
        if len(lists) == 1:
            map_content['name'] = o
        elif len(lists) == 2:
            map_content['name'] = lists[0]
            map_content['sortid'] = lists[1]
        elif len(lists) == 3:
            map_content['name'] = lists[0]
            map_content['sortid'] = lists[1]
            map_content['style'] = lists[2]
        headers.append(map_content)

    return {
        'headers': headers,
        'ordering': ordering,
        'order_by': order_by,
        'operation_style': operation_style
    }
