from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from . import forms
from . import models
import datetime
import hashlib

@login_required(login_url="/login/")
def lecture_delete(request, lecture_id):
    lecture = models.Lecture.objects.get(id=lecture_id)
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
        form.fields['module'].queryset = models.Module.objects.filter(professor=request.user.id)
        return render(request, 'lectures/lecture_create.html', {'form':form})
    

@login_required(login_url="/login/")
def lecture_list(request):
    #Get all lectures
    lectures = models.Lecture.objects.all().order_by('datetime')

    #Get all modules this user has access to
    modules = models.Module.objects.all().filter(professor=request.user.id)
    moduleIds = [module.id for module in modules]

    #User's lectures
    usersLectures = []

    for lecture in lectures:
        if (lecture.module.id in moduleIds):
            usersLectures.append(lecture)

    return render(request, 'lectures/lecture_list.html', {'lectures': usersLectures})

@login_required(login_url="/login/")
def lecture_details(request, lecture_id):
    lecture = models.Lecture.objects.get(id=lecture_id)
    qr_code_str = get_qr_code(lecture.secret)
    return render(request, 'lectures/lecture_details.html', {'lecture': lecture, 'qr_code_str':qr_code_str})

@login_required(login_url="/login/")
def lecture_qr_code(request, lecture_id):
    lecture = models.Lecture.objects.get(id=lecture_id)
    qr_code_str = get_qr_code(lecture.secret)
    return render(request, 'lectures/lecture_qr_code.html', {'qr_code_str':qr_code_str})

@login_required(login_url="/login/")
def module_list(request):
    modules = models.Module.objects.all().filter(professor = request.user.id)
    return render(request, 'lectures/modules_list.html', {'modules': modules})

@login_required(login_url="/login/")
def module_details(request, module_id):
    module = models.Module.objects.get(id=module_id)
    studentAllocations = models.Allocation.objects.all().filter(module=module)
    students = [allocation.student for allocation in studentAllocations]
    return render(request, 'lectures/module_details.html', {'module': module, 'students':students})

@login_required(login_url="/login/")
def student_list(request):
    #Get all allocations for the above modules
    allocations = models.Allocation.objects.all().filter(module__professor=request.user.id)

    students = set([allocation.student for allocation in allocations])

    return render(request, 'lectures/students_list.html', {'students': students})

@login_required(login_url="/login/")
def student_details(request, student_id):
    student = models.Student.objects.get(id=student_id)

    #Get all allocations for the above modules
    allocations = models.Allocation.objects.all().filter(module__professor=request.user.id)

    modules = set([allocation.module for allocation in allocations])

    return render(request, 'lectures/student_details.html', {'student': student, 'modules':modules})

def get_qr_code(secret):
    hasher = hashlib.sha256()
    hasher.update(secret.encode("UTF-8"))

    secret_hashed = hasher.hexdigest()

    hasher.update(str(datetime.datetime.now().timestamp()//3).encode("UTF-8"))

    time_hashed = hasher.hexdigest()
    
    hasher.update((str(secret_hashed) + "-" + str(time_hashed)).encode("UTF-8"))

    return hasher.hexdigest()