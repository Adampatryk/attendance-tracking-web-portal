from .models import *

import hashlib
import datetime

def get_modules_for_student(student):
    #Get all allocations for this student
    enrolledStudents = Enrollment.objects.all().filter(student=student)

    #Retrieve modules for this student
    modules = set([allocation.module for allocation in enrolledStudents])

    return modules

def get_students_for_module(module):
    #Get all allocations for this student
    allocations = Enrollment.objects.all().filter(module=module)

    #Retrieve modules for this student
    students = set([allocation.student for allocation in allocations])

    return students

def get_professors_for_module(module):
    
    #Get allocations for all the modules this user teaches
    teachingAllocations = Teaching.objects.all().filter(module=module)
    
    #Get all the professors
    professors = [allocation.professor for allocation in teachingAllocations]

    return professors

def get_students_for_user(user):
    #Get allocations for all the modules this user teaches
    teachingAllocations = Teaching.objects.all().filter(professor=user)

    #Get all the modules
    modules = [allocation.module for allocation in teachingAllocations]

    #Retrieve the students
    students_for_user = []

    #For each module get the students and append
    for module in modules:
        students_for_user += get_students_for_module(module)

    return set(students_for_user)

def get_modules_for_user(user):
    #Get all allocated modules
    teachingAllocations = Teaching.objects.all().filter(professor=user)

    #Retrieve modules
    modules = [allocation.module for allocation in teachingAllocations]

    return modules

def get_lectures_for_user(user):
    #Get all lectures
    lectures = Lecture.objects.all().order_by('datetime')

    modules = get_modules_for_user(user)
    moduleIds = [module.id for module in modules]

    #User's lectures
    users_lectures = Lecture.objects.all().filter(module__id__in = moduleIds)

    return users_lectures

def get_qr_code(secret):
    hasher = hashlib.sha256()
    hasher.update(secret.encode("UTF-8"))

    secret_hashed = hasher.hexdigest()

    hasher.update(str(datetime.datetime.now().timestamp()//3).encode("UTF-8"))

    time_hashed = hasher.hexdigest()
    
    hasher.update((str(secret_hashed) + "-" + str(time_hashed)).encode("UTF-8"))

    return hasher.hexdigest()