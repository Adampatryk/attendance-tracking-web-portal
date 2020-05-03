from . import models

import hashlib
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"

def get_lectures_for_student(student):
    #Get all the modules that this student is taught
    modules = get_modules_for_student(student)

    return models.Lecture.objects.filter(module__in = modules).defer('secret')

# def get_modules_for_student(student):
#     #Get all allocations for this student
#     enrolledStudents = models.Enrollment.objects.all().filter(student=student)

#     #Retrieve modules for this student
#     modules = set([allocation.module for allocation in enrolledStudents])

#     return modules

def get_students_for_module(module):
    #Get all allocations for this student
    allocations = models.Enrollment.objects.all().filter(module=module)

    student_ids = []

    for allocation in allocations:
        student_ids.append(allocation.student.id)

    students_for_module = models.User.objects.filter(id__in=student_ids)

    return students_for_module

def get_professors_for_module(module):
    
    #Get allocations for all the modules this user teaches
    teachingAllocations = models.Teaching.objects.all().filter(module=module)
    
    #Get all the professors
    professors = [allocation.professor for allocation in teachingAllocations]

    return professors

def get_students_for_user(user):
    #Get allocations for all the modules this user teaches
    teachingAllocations = models.Teaching.objects.all().filter(professor=user)

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
    if (user.usertypewrapper.is_lecturer == True):
        allocations = models.Teaching.objects.all().filter(professor=user)
    else:
        allocations = models.Enrollment.objects.all().filter(student=user)
    
    #Retrieve modules that are active
    modules = []
    
    for allocation in allocations:
        if (allocation.module.active):
            modules.append(allocation.module)

    return modules

def get_lectures_for_user(user, date=False, modules=None):

    if (modules == None):
        #Get all the modules for the user
        modules = get_modules_for_user(user)

    #User's lectures
    users_lectures = models.Lecture.objects.filter(module__in = modules).order_by("datetime")

    #If a date is specified then filter
    if (date != False):
        users_lectures = users_lectures.filter(datetime__year=date.year, datetime__month=date.month, datetime__day=date.day)

    #If user is a student 
    if (not user.usertypewrapper.is_lecturer):
        # get the all attendances for this user
        for lecture in users_lectures:
            try:
                att = models.Attendance.objects.get(lecture=lecture, student=user).present
                if (att):
                    lecture.setPresent(1)
                else:
                    lecture.setPresent(0)
                
            except models.Attendance.DoesNotExist:
                lecture.setPresent(-1)
            
            #Set secret to null
            lecture.secret = None

    return users_lectures

def get_lectures_for_module(module):
    #Get all lectures for this module
    lectures = models.Lecture.objects.filter(module=module).order_by('datetime')

    return lectures

#Get all students for a specific lecture and whether they attended or not
def get_attendance_for_lecture(lecture):
    records = models.Attendance.objects.filter(lecture=lecture)

    return records

#Return a number between 0 and 1 representing the percentage of all records that this student has attended for this module
def get_attendance_percentage_for_student_for_module(student, module):
    #Get all the attendance records for this user for this module
    all_attendances_for_module = models.Attendance.objects.filter(student=student, lecture__in=get_lectures_for_module(module))

    #Get all of those which are present
    present_attendances_for_modules = all_attendances_for_module.filter(present=True)

    #Prevent division by 0
    if all_attendances_for_module.count() == 0: 
        return 0
    else: 
        return present_attendances_for_modules.count() / all_attendances_for_module.count()


def get_upcoming_lectures_for_module(module):
    #Get all lectures for module
    lecturesForModule = get_lectures_for_module(module)

    #Filter for all lectures that are happening in the future
    upcomingLectures = lecturesForModule.filter(datetime__gt=datetime.now()).order_by('-datetime')

    return upcomingLectures

def is_valid_timestamp(timestamp):
    now = int(datetime.now().timestamp()//3)

    #If the timestamp is older than now
    if (timestamp < now - 1):
        print(timestamp, now)
        return False
    else:
        return True

def get_qr_code(secret, time=False):
    if (not time):
        time = datetime.now().timestamp()//3

    #Get all the hashers
    secretHasher = hashlib.sha256()
    timeHasher = hashlib.sha256()
    combinedHashed = hashlib.sha256()

    #Hash the secret
    secretHasher.update(secret.encode("UTF-8"))
    secret_hashed = secretHasher.hexdigest()

    #Hash the timestamp
    timestamp = str(int(time))
    timeHasher.update(timestamp.encode("UTF-8"))
    time_hashed = timeHasher.hexdigest()
    
    #Hash the combination
    combinedHashed.update((secret_hashed + "-" + time_hashed).encode("UTF-8"))
    return combinedHashed.hexdigest()