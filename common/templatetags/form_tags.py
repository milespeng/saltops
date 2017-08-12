from django import template

register = template.Library()


@register.inclusion_tag("common/tags/form_text_field.html")
def form_text_field(label, form, error_msg):
    return {
        'label': label,
        'form': form,
        'error_msg': error_msg
    }


@register.inclusion_tag("common/tags/form_raw_text_field.html")
def form_raw_text_field(label, id, value, name, placeholder, error_msg):
    return {
        'label': label,
        'id': id,
        'name': name,
        'placeholder': placeholder,
        'value': value,
        'error_msg': error_msg
    }


@register.inclusion_tag("common/tags/form_submit_btns.html")
def form_submit_btns(submit_btn_name="保存", extra_btns=""):
    return {
        'submit_btn_name': submit_btn_name,
        'extra_btns': []
    }


@register.inclusion_tag("common/tags/form_select_fields.html")
def form_select_fields(label, placeholder, id, datasource, selected_field):
    return {
        'label': label,
        'placeholder': placeholder,
        'id': id,
        'datasource': datasource,
        'selected_field': selected_field
    }


@register.inclusion_tag("common/tags/form_script_field.html")
def form_script_field(label, id, content, readonly=False, language_type=0):
    return {
        'label': label,
        'id': id,
        'content': content,
        'readonly': readonly,
        'language_type': language_type
    }
