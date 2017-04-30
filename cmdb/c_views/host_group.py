from http.client import HTTPResponse
import better_exceptions
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import register
from django.db.models import Model
from django.forms import *
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods

from cmdb.models import *
from common.pageutil import preparePage

