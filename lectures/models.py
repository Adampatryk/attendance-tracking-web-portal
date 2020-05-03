from django.db import models
from login.models import UserTypeWrapper
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.utils.crypto import get_random_string

from django.utils import timezone

from . import utils

#Change the user string representation
def custom_user_display(self):
    return self.first_name + " " + self.last_name + " (" + self.username + ")" 

User.add_to_class("__str__", custom_user_display) # override the __unicode__ method


#Represents a class of students being taught by a specific professor for a specific module
class Module(models.Model):
    title = models.CharField(max_length=50, unique=True)
    moduleCode = models.CharField(unique=True, max_length=16)
    academicYearStart = models.DateField()
    active = models.BooleanField()
    weight = models.IntegerField()
    info = models.TextField(max_length=5000, null=False, blank=True)

    def __str__(self):
        return self.title


#Represents a single lecture for a class
class Lecture(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    secret = models.CharField(max_length=64)
    info = models.TextField(max_length=5000, null=False, blank=True)
    isPresent = -1

    def __str__(self):
        return self.module.title + " - " + self.title

    def save(self, *args, **kwargs):
        self.secret = get_random_string(length=64)
        super(Lecture, self).save(*args, **kwargs)

    def setPresent(self, present):
        self.isPresent = present

    def getPresent(self):
        return self.isPresent

    def getModuleId(self):
        return self.module.id

#This is called whenever a new lecture is created
@receiver(post_save, sender=Lecture)
def create_lecture_attendance_records(sender, instance=None, created=False, **kwargs):
    if created:
        studentsForLecture = utils.get_students_for_module(instance.module)
        for student in studentsForLecture:
            Attendance.objects.create(student=student, 
                                        lecture=instance,
                                        present=False,
                                        timestamp=None,
                                        deviceId=None)

#Represents a student being a part of a module
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'module')


#This creates an attendance record for a newly created Enrollment for a student, 
# in all the upcoming lectures for that module
@receiver(post_save, sender=Enrollment)
def create_lecture_attendance_record_for_new_enrollment(sender, instance=None, created=False, **kwargs):
    if created:
        #Find all upcoming lectures for this student for this module 
        upcomingLectures = utils.get_upcoming_lectures_for_module(instance.module)

        for lecture in upcomingLectures:
            #If the student doesn't already have an attendance record ready, add it
            if (Attendance.objects.filter(student=instance.student, lecture=lecture).count() == 0):
                Attendance.objects.create(student=instance.student,
                                            lecture=lecture,
                                            present=False,
                                            timestamp=None,
                                            deviceId=None)

#This deletes attendance records for the student on this module for all upcoming lectures
@receiver(post_delete, sender=Enrollment)
def delete_lecture_attendance_record_for_deleted_enrollment(sender, instance=None, created=False, **kwargs):
    #Find all upcoming lectures for this student for this module 
    upcomingLectures = utils.get_upcoming_lectures_for_module(instance.module)

    #Find all attendance records for the upcoming lectures for this student and delete them
    Attendance.objects.filter(student=instance.student, lecture__in=upcomingLectures).delete()


#Represents a professor teaching a module
class Teaching(models.Model):
    professor = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('professor', 'module')

#Each row represents a student being present at a certain lecture
class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True)
    deviceId = models.CharField(max_length=16, null=True)

    def save(self, *args, **kwargs): 
        if self.present:
            self.timestamp = timezone.now()
        else:
            self.deviceId = None
            self.timestamp = None
        super(Attendance, self).save(*args, **kwargs)

    class Meta:
        unique_together =(('student', 'lecture'), ('lecture', 'deviceId'))

    def __str__(self):
        return "'" + self.student.__str__() + "'" + " attending '" + self.lecture.__str__() + "'"