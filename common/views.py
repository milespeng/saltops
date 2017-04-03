from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    context = {}
    if 'type' in request.GET:
        context['type'] = request.GET['type']
    return render(request, 'frontend/index.html', context)


def checkLogin(request, authentication_form=AuthenticationForm):
    form = authentication_form(request, data=request.POST)
    if form.is_valid():
        return redirect('/mainform/')
    else:
        return redirect('/?type=1')


def mainform(request):
    return render(request, 'frontend/mainform.html', {})
