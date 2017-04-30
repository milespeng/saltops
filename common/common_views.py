from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods
import better_exceptions
from common.pageutil import preparePage


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_list(request, args):
    kwargs = dict(filter(lambda x: x[1] != '', request.GET.dict().items()))
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    if 'plugin_name' in args:
        plugin = getattr(getattr(module, 'c_views'), args['plugin_name'])
        plugin_result = plugin()
    obj = instance.objects.filter(**kwargs)
    result_list = preparePage(request, obj)
    return render(request, args['template_path'], locals(), RequestContext(request))


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_delete_entity(request, pk, args):
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    if 'plugin_name' in args:
        plugin = getattr(getattr(module, 'c_views'), args['plugin_name'])
        plugin_result = plugin()
    instance.objects.filter(pk=pk).delete()
    return redirect(args['list_url'])


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_batch_delete_entity(request, args):
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    ids = request.GET['id'][:-1].split(',')
    if 'delete_plugin' in args:
        plugin = getattr(getattr(module, 'c_views'), args['delete_plugin'])
        plugin_result = plugin()
    instance.objects.filter(pk__in=ids).delete()
    return HttpResponse("")


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_add(request, args):
    action = args['add_action']
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    if 'add_fields' not in args:
        form = modelform_factory(instance, fields='__all__')
    else:
        form = modelform_factory(instance, fields=(args['add_fields'].split(',')))
    title = args['add_title']
    if 'add_form_plugin' in args:
        plugin = getattr(getattr(module, 'c_views'), args['add_form_plugin'])
        plugin_result = plugin(locals())
    return render(request, args['form_template_path'], locals(), RequestContext(request))


@require_http_methods(["POST"])
@gzip_page
@login_required
def simple_add_action(request, args):
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    form = modelform_factory(instance, fields='__all__')
    form = form(request.POST)
    if 'add_action_plugin' in args:
        plugin = getattr(getattr(module, 'c_views'), args['add_action_plugin'])
        plugin_result = plugin()
    if form.is_valid():
        form.save()
        return redirect(args['list_url'])
    else:
        return render(request, args['form_template_path'], locals())


@require_http_methods(["GET"])
@gzip_page
@login_required
def simple_edit(request, pk, args):
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    if 'edit_fields' not in args:
        form = modelform_factory(instance, fields='__all__')
    else:
        form = modelform_factory(instance, fields=(args['edit_fields'].split(',')))
    title = args['edit_title']
    action = args['edit_action'] % pk
    entity = get_object_or_404(instance, pk=pk)
    form = form(instance=entity)
    if 'edit_form_plugin' in args:
        plugin = getattr(getattr(module, 'c_views'), args['edit_form_plugin'])
        plugin_result = plugin(locals())
    return render(request, args['form_template_path'], locals())


@require_http_methods(["POST"])
@gzip_page
@login_required
def simple_edit_action(request, pk, args):
    module = __import__(args['modulename'])
    instance = getattr(getattr(module, 'models'), args['modelname'])
    entity = get_object_or_404(instance, pk=pk)
    form = modelform_factory(instance, fields='__all__')
    form = form(request.POST, instance=entity)
    if 'edit_action_plugin' in args:
        plugin = getattr(getattr(module, 'c_views'), args['edit_action_plugin'])
        plugin_result = plugin()
    if form.is_valid():
        form.save()
        return redirect(args['list_url'])
    else:
        return render(request, args['form_template_path'], locals())
