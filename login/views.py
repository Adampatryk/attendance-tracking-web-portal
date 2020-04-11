from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from login import models

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            #if user is a student account, deny login
            print("User is a lecturer test: ", user.usertypewrapper.is_lecturer)
            if (user.usertypewrapper.is_lecturer):
                login(request, user)
                username = request.user.username
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('lectures:list')
            else:
                form.add_error(None, "Access denied")
            
        return render(request, 'login/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login/login.html', {'form': form})

@login_required(login_url="login/")
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login:login')
