# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    reg_form = UserRegForm()
    log_form = LoginForm()
    return render(request, "login_register/index.html", {"reg_form": reg_form, "log_form": log_form})

def success(request):
    if not "user_id" in request.session:
        return redirect(index)
    user = User.objects.get(id=request.session["user_id"])
    return render(request, "login_register/success.html", {"user": user})

def register(request):
    if request.method != "POST":
        return redirect(index)
    form = UserRegForm(request.POST)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.encrypt_password()
        new_user.save()
        request.session["user_id"] = new_user.id
        messages.success(request, "Successfully registered!")
        return redirect(success)
    else:
        messages.error(request, form.errors)
    return redirect(index)

def login(request):
    if request.method != "POST":
        return redirect(index)
    form = LoginForm(request.POST)
    if form.is_valid():
        users = User.objects.filter(email=form.cleaned_data["email"])
        if len(users) < 1:
            messages.error(request, "Email or password is incorrect")
            return redirect(index)
        user = users[0]
        pw = form.cleaned_data["password"]
        if user.check_password(pw):
            request.session["user_id"] = user.id
            messages.success(request, "Successfully logged in!")
            return redirect(success)
        else:
            messages.error(request, "Email or password is incorrect")
    else:
        messages.error(request, form.errors)
    return redirect(index)

def logout(request):
    request.session.flush()
    return redirect(index)