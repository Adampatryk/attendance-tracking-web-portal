from django.db import models
from django.contrib.auth.models import User

#Represents a class of students being taught by a specific professor for a specific module
class Module(models.Model):
    title = models.CharField(max_length=50, unique=True)
    moduleCode = models.IntegerField(unique=True)
    academicYearStart = models.DateField()
    active = models.BooleanField()

    def __str__(self):
        return self.title


#Represents a single lecture for a class
class Lecture(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    secret = models.CharField(max_length=64)

#Represents a students
class Student(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    studentId = models.IntegerField(unique=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

#Represents a student being a part of a module
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'module')

#Represents a professor teaching a module
class Teaching(models.Model):
    professor = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('professor', 'module')