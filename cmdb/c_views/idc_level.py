from django.shortcuts import render


def idc_level_list(request):
    return render(request, 'frontend/cmdb/idc_level_list.html', {
    })
