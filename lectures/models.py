from django.db import models
from django.contrib.auth.models import User

#Represents a class of students being taught by a specific professor for a specific module
class Module(models.Model):
    title = models.CharField(max_length=50)
    professorId = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    moduleCode = models.IntegerField()
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
