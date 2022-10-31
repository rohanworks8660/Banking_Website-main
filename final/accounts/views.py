# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.forms import modelform_factory

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from profiles.models import UserInfo
from .forms import NewForm, Ourform
from django.contrib.auth.models import User
import os

NewForm = modelform_factory(UserInfo, exclude=[])


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        #ourform = Ourform(request.POST)
        UInf = NewForm(request.POST)
        if form.is_valid() and UInf.is_valid():
            form.save()
            # ourform.save()
            
            UInf.save()
            return redirect("accounts:signin")
    else:
        form = UserCreationForm()
        #ourform = Ourform()
        UInf = NewForm()
    return render(request, "accounts/create_account.html", {"form": form,  "UInf": UInf})



def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # return redirect("profiles:account_status")
            return redirect("profiles:dashboard")
    else:
        form = AuthenticationForm()
        # print('invalid')
    return render(request, "accounts/sign_in.html", {"form": form})
    # return redirect("accounts:signin")


def logout_view(request):
    # Logout the user if he hits the logout submit button
    logout(request)
    return redirect("accounts:signin")


def homepage(request):
    # Logout the user if he hits the logout submit button
    logout(request)
    cwd=os.getcwd
    return render(request, "accounts/homepage.html",{"cwd":cwd})
