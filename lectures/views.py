from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.http import HttpResponseForbidden, HttpResponseNotFound
from .utils import *

from . import forms
from . import models

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
        modules = get_modules_for_user(request.user)
        module_ids = [module.id for module in modules]
        form.fields['module'].queryset = models.Module.objects.all().filter(pk__in = module_ids)
        return render(request, 'lectures/lecture_create.html', {'form':form})
    

@login_required(login_url="/login/")
def lecture_list(request):
    
    users_lectures = get_lectures_for_user(request.user)

    return render(request, 'lectures/lecture_list.html', {'lectures': users_lectures})

@login_required(login_url="/login/")
def lecture_details(request, lecture_id):
    #Get the lecture, return 404 if not found
    try:
        lecture = models.Lecture.objects.get(id=lecture_id)
    except models.Lecture.DoesNotExist:
        return HttpResponseNotFound()

    users_lectures = get_lectures_for_user(request.user)
    
    #If this is not a lecture that the user teaches, return Forbidden
    if (lecture not in users_lectures):
        return HttpResponseForbidden()  
    else:
        #Get QR Code for this lecture
        qr_code_str = get_qr_code(lecture.secret)
        return render(request, 'lectures/lecture_details.html', {'lecture': lecture, 'qr_code_str':qr_code_str})

@login_required(login_url="/login/")
def lecture_qr_code(request, lecture_id):
    users_lectures = get_lectures_for_user(request.user)

    #Get the lecture, return 404 if not found
    try:
        lecture = models.Lecture.objects.get(id=lecture_id)
    except models.Lecture.DoesNotExist:
        return HttpResponseNotFound()
    
    #If this is not a lecture that the user teaches, return Forbidden
    if (lecture not in users_lectures):
        return HttpResponseForbidden()  
    else:
        #Get QR Code for this lecture
        qr_code_str = get_qr_code(lecture.secret)
        return render(request, 'lectures/lecture_qr_code.html', {'qr_code_str':qr_code_str})

@login_required(login_url="/login/")
def module_list(request):
    modules = get_modules_for_user(request.user)
    return render(request, 'lectures/modules_list.html', {'modules': modules})

@login_required(login_url="/login/")
def module_details(request, module_id):
    #Get the module, return 404 if not found
    try: 
        module = models.Module.objects.get(id=module_id)

        #Get all modules
        modules_for_user = get_modules_for_user(request.user)
        #If the user does not teach this module, restrict access
        if (module not in modules_for_user):
            return HttpResponseForbidden()

    except models.Module.DoesNotExist:
        return HttpResponseNotFound()

    #Get all allocations for this module
    studentAllocations = models.Enrollment.objects.all().filter(module=module)
    #Get students from the allocations
    students = [allocation.student for allocation in studentAllocations]
    return render(request, 'lectures/module_details.html', {'module': module, 'students':students})

@login_required(login_url="/login/")
def student_list(request):

    students = get_students_for_user(request.user)

    return render(request, 'lectures/students_list.html', {'students': students})

@login_required(login_url="/login/")
def student_details(request, student_id):
    #Get the student, 404 if not found
    try:
        student = models.Student.objects.get(id=student_id)

        #Check if this student is taught by this user
        students_for_user = get_students_for_user(request.user)

        #If student not taught by user, forbid access
        if student not in students_for_user:
            return HttpResponseForbidden()

    except models.Student.DoesNotExist:
        return HttpResponseNotFound()

    modules = get_modules_for_student(student)

    return render(request, 'lectures/student_details.html', {'student': student, 'modules':modules})