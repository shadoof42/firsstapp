# -*- coding: utf-8 -*-
from django.contrib import auth
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from django.template.context_processors import csrf


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/articles/page/1/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html',args)
    else:
        return render_to_response('login.html',args)


def logout(request):
    auth.logout(request)
    return redirect('/articles/page/1/')

def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username = newuser_form.cleaned_data['username'],password = newuser_form.cleaned_data['password2'])
            auth.login(request,newuser)
            return redirect('/articles/page/1/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)