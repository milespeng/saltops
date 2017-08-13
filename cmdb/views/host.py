import requests
from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from saltjob.tasks import scanHostJob
from saltops.settings import PER_PAGE, SALT_HTTP_URL, SALT_CONN_TYPE


def updateSaltRouster():
    # 如果主机是SSH类型的，把SSH列表更新一遍
    hosts = Host.objects.all()

    rosterString = ""
    for host in hosts:
        if host.enable_ssh is True:
            rosterString += """

%s:
    host: %s
    user: %s
    passwd: %s
    sudo: %s
    tty: True

                    """ % (host.host, host.host, host.ssh_username, host.ssh_password,
                           host.enable_ssh)

    if SALT_CONN_TYPE == 'http':
        requests.post(SALT_HTTP_URL + '/rouster', data={'content': rosterString})
    else:
        with open('/etc/salt/roster', 'w') as content:
            content.write(rosterString)


class HostView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Host
    paginate_by = PER_PAGE
    template_name = 'cmdb/host_list.html'
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['parent', 'name', 'idc', 'os', 'enable_ssh', 'minion_status',
                         'create_time', 'update_time']

    def get_queryset(self):
        result_list = Host.objects.all()
        host = self.request.GET.get('host')
        ip_filter = self.request.GET.get('ip_filter')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)
        if host:
            result_list = result_list.filter(host__contains=host)
        if ip_filter:
            host_ip_lists = HostIP.objects.filter(ip__contains=ip_filter)
            host_filter_list = []
            for k in host_ip_lists:
                host_filter_list.append(k.host)
            result_list = result_list.filter(host_name__in=host_filter_list)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(HostView, self).get_context_data(**kwargs)
        context['host'] = self.request.GET.get('host', '')
        context['ip_filter'] = self.request.GET.get('ip_filter', '')
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        return context


class HostCreateView(LoginRequiredMixin, CreateView):
    model = Host
    form_class = HostForm
    template_name = 'cmdb/host_form.html'
    success_url = reverse_lazy('cmdb:host_list')

    def get_context_data(self, **kwargs):
        context = super(HostCreateView, self).get_context_data(**kwargs)
        context['is_add'] = True
        return context

    def form_valid(self, form):
        obj = form.save()
        updateSaltRouster()
        host_ips = zip(self.request.POST.getlist('ip'), self.request.POST.getlist('ip_type'))
        for o in list(host_ips):
            HostIP(ip=o[0], ip_type=o[1], host=obj).save()
        return super(HostCreateView, self).form_valid(form)


class HostUpdateView(LoginRequiredMixin, UpdateView):
    model = Host
    form_class = HostForm
    template_name = 'cmdb/host_form.html'
    success_url = reverse_lazy('cmdb:host_list')
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(HostUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        obj = self.object
        cabinet_list = Cabinet.objects.filter(idc=obj.idc)
        context['cabinet_list'] = cabinet_list
        context['rack_list'] = Rack.objects.filter(cabinet__in=cabinet_list)
        context['host_ip_list'] = HostIP.objects.filter(host=obj)
        return context

    def form_valid(self, form):
        obj = form.save()
        updateSaltRouster()
        HostIP.objects.filter(host=obj).delete()
        host_ips = zip(self.request.POST.getlist('ip'), self.request.POST.getlist('ip_type'))
        for o in list(host_ips):
            HostIP(ip=o[0], ip_type=o[1], host=obj).save()
        return super(HostUpdateView, self).form_valid(form)


class HostDeleteView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Host.objects.filter(pk__in=map(int, ids.split(','))).delete()
            updateSaltRouster()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})


class ScanHostJobView(LoginRequiredMixin, JSONResponseMixin,
                      AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        scanHostJob()
        return self.render_json_response({})
