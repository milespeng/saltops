from django.template.defaultfilters import register
from django.utils.safestring import mark_safe


@register.filter()
def str_to_int(value):
    if value is not None:
        return int(value)
    else:
        return value


@register.filter()
def replace_to_br(value: str):
    return mark_safe(value.replace('\n', '<br/>'))
