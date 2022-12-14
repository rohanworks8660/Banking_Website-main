# Create your views here.
import os
from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import NewForm
from profiles.models import UserInfo


NewForm = modelform_factory(UserInfo, exclude=["username"])


pswd = ""

def services(request):
    return render(request, "accounts/services.html")

def aboutus(request):
    return render(request, "accounts/aboutus.html")

def contactus(request):
    return render(request, "accounts/contactus.html")

def register(request):
    global uname
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        uname = str(request.POST.get('username'))
        if form.is_valid():
            form.save()
            return redirect("accounts:signup2")
    else:
        form = UserCreationForm()
    return render(request, "accounts/create_account.html", {"form": form})


def update_username(uname, firstname):
    a = UserInfo.objects.get(first_name=firstname)
    a.username = uname
    a.save()

def register2(request):
    global uname
    if request.method == "POST":
        UInf = NewForm(request.POST)
        if UInf.is_valid():
            firstname = str(request.POST.get('first_name'))
            UInf.save()
            update_username(uname, firstname)
            return redirect("accounts:signin")
    else:
        UInf = NewForm()
    return render(request, "accounts/create_account2.html", {"UInf": UInf, "uname": uname})


def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profiles:dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/sign_in.html", {"form": form})


def logout_view(request):
    # Logout the user if he hits the logout submit button
    logout(request)
    return redirect("accounts:signin")


def homepage(request):
    # Logout the user if he hits the logout submit button
    logout(request)
    cwd = os.getcwd
    return render(request, "accounts/homepage.html", {"cwd": cwd})
