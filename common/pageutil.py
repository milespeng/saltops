from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import better_exceptions


def preparePage(request, dataList):
    page = 1
    if 'page' in request.GET:
        page = int(request.GET['page'])
    paginator = Paginator(dataList, 10)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list
