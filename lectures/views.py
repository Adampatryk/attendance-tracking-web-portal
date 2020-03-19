from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from . import forms
from . import models
import datetime
import hashlib

@login_required(login_url="/login/")
def lecture_delete(request, id):
    lecture = models.Lecture.objects.get(id=id)
    lecture.delete()
    return redirect('lectures:list')

@login_required(login_url="/login/")
def lecture_create(request):
    if request.method == "POST":
        form = forms.CreateLecture(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.secret = get_random_string(length=64)
            instance.save()
            return redirect('lectures:list')
    else:
        form = forms.CreateLecture()
        return render(request, 'lectures/lecture_create.html', {'form':form})
    

@login_required(login_url="/login/")
def lecture_list(request):
    lectures = models.Lecture.objects.all().order_by('datetime')

    return render(request, 'lectures/lecture_list.html', {'lectures': lectures})

@login_required(login_url="/login/")
def lecture_details(request, id):
    lecture = models.Lecture.objects.get(id=id)
    qr_code_str = get_qr_code(lecture.secret)
    return render(request, 'lectures/lecture_details.html', {'lecture': lecture, 'qr_code_str':qr_code_str})

def lecture_qr_code(request, id):
    lecture = models.Lecture.objects.get(id=id)
    qr_code_str = get_qr_code(lecture.secret)
    return render(request, 'lectures/lecture_qr_code.html', {'qr_code_str':qr_code_str})

def get_qr_code(secret):
    hasher = hashlib.sha256()
    hasher.update(secret.encode("UTF-8"))

    secret_hashed = hasher.hexdigest()

    hasher.update(str(datetime.datetime.now().timestamp()//3).encode("UTF-8"))

    time_hashed = hasher.hexdigest()
    
    hasher.update((str(secret_hashed) + "-" + str(time_hashed)).encode("UTF-8"))

    return hasher.hexdigest()