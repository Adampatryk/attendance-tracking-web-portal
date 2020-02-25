from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            username = request.user.username
            return HttpResponse("<h1>Hello " + username + "</h1>")
        return render(request, 'login/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login/login.html', {'form': form})