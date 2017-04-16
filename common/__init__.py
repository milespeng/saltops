from django.template.defaultfilters import register


@register.filter()
def str_to_int(value):
    if value is not None:
        return int(value)
    else:
        return value
