from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            username = request.user.username
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('lectures:list')
        return render(request, 'login/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login/login.html', {'form': form})

@login_required(login_url="login/")
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login:login')
