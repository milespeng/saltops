import platform
import better_exceptions
import psutil
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from cmdb.models import Host
from deploy_manager.models import Project


def index(request):
    """
    登录页面
    :param request:
    :return:
    """
    context = {}
    if 'type' in request.GET:
        context['type'] = request.GET['type']
    return render(request, 'frontend/index.html', context)


def checkLogin(request):
    """
    登录校验，使用Django默认的用户权限模块
    :param request:
    :param authentication_form:
    :return:
    """
    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
    if user and user.is_active:
        auth.login(request, user)
        return redirect('/mainform/')
    else:
        return redirect('/?type=1')


def logout(request):
    auth.logout(request)
    return render(request, 'login/login.html', context={
        'info': "登出成功"
    })


def mainform(request):
    """
    系统主窗体
    :param request:
    :return:
    """
    return render(request, 'frontend/mainform.html', {})


def dashboard(request):
    """
    首页仪表盘
    :param request:
    :return:
    """
    module = {}

    # 系统基础配置
    upMinionCount = Host.objects.filter(minion_status=1).count()
    downMinionCount = Host.objects.filter(minion_status=0).count()
    module['hostname'] = platform.node()
    module['system_info'] = '%s, %s, %s' % (
        platform.system(),
        ' '.join(platform.linux_distribution()),
        platform.release())
    module['arch'] = ' '.join(platform.architecture())
    module['procesor'] = platform.processor(),
    module['py_version'] = platform.python_version()
    module['host_count'] = Host.objects.count()
    module['buss_count'] = Project.objects.count()
    module['minions_status'] = '运行中 %s,未运行 %s' % (upMinionCount, downMinionCount)

    # 资源使用率
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    green, orange, red, grey = '#00FF38', '#FFB400', '#FF3B00', '#EBEBEB'

    ram_color = green
    if ram >= 75:
        ram_color = red
    elif ram >= 50:
        ram_color = orange

    cpu_color = green
    if cpu >= 75:
        cpu_color = red
    elif cpu >= 50:
        cpu_color = orange

    module['cpu_idel'] = 100 - cpu
    module['cpu_color'] = cpu_color
    module['cpu'] = cpu
    module['ram'] = 100 - ram
    module['ram_used'] = ram
    module['ram_color'] = ram_color

    # 操作系统分布
    result = Host.objects.values('os').annotate(total=Count('os'))

    os = []
    total = []
    for obj in result:
        os.append(obj['os'])
        total.append(obj['total'])
    module['os'] = os
    module['total'] = total
    return render(request, 'frontend/dashboard.html', {
        'module': module
    })
