# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, SignupFormStep1, SignupFormStep2, SignupFormStep3
from apps.models import Organization, User

from core.settings import GITHUB_AUTH

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg, "GITHUB_AUTH": GITHUB_AUTH})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Account created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def start_signup(request):
    msg = None
    success = False
    return render(request, "accounts/pricing.html", {"msg": msg, "success": success})

def create_account(request):
    msg = None
    success = False
    #TODO if the user is already logged in - then move them to the right stage automatically
    if request.method == "POST":
        if request.POST.get('email'):
            form = SignupFormStep1(request.POST)
            if form.is_valid():
                try:
                    user_obj = User.objects.get(email = form.cleaned_data.get("email"))
                except:
                    new_user = User(username=form.cleaned_data.get("email"), email=form.cleaned_data.get("email"),password=form.cleaned_data.get("password"))
                    #TODO encrypt password
                    new_user.save()
                    #TODO email with auth code will need to be sent to the user
                    login(request,new_user,backend='core.custom-auth-backend.CustomBackend')
                    form = SignupFormStep2()
                    return render(request, "accounts/reg-step-2.html", {"msg": msg, "success": True, "form": form})
                if user_obj.password == form.cleaned_data.get("password"):
                    login(request, user_obj,backend='core.custom-auth-backend.CustomBackend')
                    form = SignupFormStep2()
                    #TODO depending on the stage of the user - like email already entered, etc the right redirections need to be done
                    return render(request, "accounts/reg-step-2.html", {"msg": msg, "success": True, "form": form})
                else:
                    msg = "This email is already registred. Enter the correct password or try with a new email"
                    return render(request, "accounts/reg-step-1.html", {"msg": msg, "success": success, "form": form})
            else:
                msg = "Pls check for errors in the form"
                return render(request, "accounts/reg-step-1.html", {"msg": msg, "success": success, "form": form})
        elif request.POST.get('auth_code'):
            #TODO check the validity of the auto code and update the status in the user model
            import pdb; pdb.set_trace()
            form = SignupFormStep3()
            return render(request, "accounts/reg-step-3.html", {"msg": msg, "success": True, "form": form})
        elif request.POST.get("org_name"):
            #TODO start the billing flow from here
            return HttpResponse(status=204)
    else:
        form = SignupFormStep1()
        return render(request, "accounts/reg-step-1.html", {"msg": msg, "success": success, "form": form})