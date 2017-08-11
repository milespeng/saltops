from django import template

register = template.Library()


@register.inclusion_tag("common/tags/form_text_field.html")
def form_text_field(label, form, error_msg):
    return {
        'label': label,
        'form': form,
        'error_msg': error_msg
    }


@register.inclusion_tag("common/tags/form_submit_btns.html")
def form_submit_btns(submit_btn_name="保存", extra_btns=""):
    return {
        'submit_btn_name': submit_btn_name,
        'extra_btns': []
    }


@register.inclusion_tag("common/tags/form_script_field.html")
def form_script_field(label, id, content):
    return {
        'label': label,
        'id': id,
        'content': content
    }
