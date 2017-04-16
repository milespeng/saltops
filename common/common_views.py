from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from common.pageutil import preparePage


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_list(request,
                modulename, modelname, list_url,
                form_template_path, template_path, add_fields,
                add_title, add_action, edit_fields, edit_title, edit_action
                ):
    kwargs = request.GET.dict()
    module = __import__(modulename)
    instance = getattr(getattr(module, 'models'), modelname)
    obj = instance.objects.filter(**kwargs)
    result_list = preparePage(request, obj)
    return render(request, template_path, locals(), RequestContext(request))


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_delete_entity(request, pk,
                         modulename, modelname, list_url,
                         form_template_path, template_path, add_fields,
                         add_title, add_action, edit_fields, edit_title, edit_action
                         ):
    module = __import__(modulename)
    instance = getattr(getattr(module, 'models'), modelname)
    instance.objects.filter(pk=pk).delete()
    return redirect(list_url)


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_batch_delete_entity(request,
                               modulename, modelname, list_url,
                               form_template_path, template_path, add_fields,
                               add_title, add_action, edit_fields, edit_title, edit_action
                               ):
    module = __import__(modulename)
    instance = getattr(getattr(module, 'models'), modelname)
    ids = request.GET['id'][:-1].split(',')
    instance.objects.filter(pk__in=ids).delete()
    return HttpResponse("")


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_add(request,
               modulename, modelname, list_url,
               form_template_path, template_path, add_fields,
               add_title, add_action, edit_fields, edit_title, edit_action
               ):
    action = add_action
    module = __import__(modulename)
    instance = getattr(getattr(module, 'models'), modelname)
    if add_fields == '__all__':
        form = modelform_factory(instance, fields='__all__')
    else:
        form = modelform_factory(instance, fields=(add_fields.split(',')))
    title = add_title
    return render(request, form_template_path, locals(), RequestContext(request))


@require_http_methods(["POST"])
@gzip_page
@login_required
def simple_add_action(request,
                      modulename, modelname, list_url,
                      form_template_path, template_path, add_fields,
                      add_title, add_action, edit_fields, edit_title, edit_action
                      ):
    module = __import__(modulename)
    instance = getattr(getattr(module, 'models'), modelname)
    form = modelform_factory(instance, fields='__all__')
    form = form(request.POST)

    if form.is_valid():
        form.save()
        return redirect(list_url)
    else:
        return render(request, form_template_path, locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_edit(request, pk,
                modulename, modelname, list_url,
                form_template_path, template_path, add_fields,
                add_title, add_action, edit_fields, edit_title, edit_action
                ):
    module = __import__(modulename)
    instance = getattr(getattr(module, 'models'), modelname)
    if edit_fields == '__all__':
        form = modelform_factory(instance, fields='__all__')
    else:
        form = modelform_factory(instance, fields=(edit_fields.split(',')))
    title = edit_title
    action = edit_action % pk
    entity = get_object_or_404(instance, pk=pk)
    form = form(instance=entity)
    return render(request, form_template_path, locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def simple_edit_action(request, pk,
                       modulename, modelname, list_url,
                       form_template_path, template_path, add_fields,
                       add_title, add_action, edit_fields, edit_title, edit_action):
    module = __import__(modulename)
    instance = getattr(getattr(module, 'models'), modelname)
    entity = get_object_or_404(instance, pk=pk)
    form = modelform_factory(instance, fields='__all__')
    form = form(request.POST, instance=entity)

    if form.is_valid():
        form.save()
        return redirect(list_url)
    else:
        return render(request, form_template_path, locals())
