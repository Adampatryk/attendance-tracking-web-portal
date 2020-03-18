from django.db import models

#Represents a single lecture for a class
class Lecture(models.Model):
    classId = models.IntegerField()
    title = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    secret = models.CharField(max_length=64)

# #Represents a class of students being taught by a specific professor for a specific module
# class Class(models.Model):
#     professorId = models.IntegerField()
#     moduleId = models.IntegerField()
#     academicYearStart = models.DateField()