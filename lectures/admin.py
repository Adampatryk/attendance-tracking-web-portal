from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('module', 'title', 'datetime', 'secret')
    list_filter = ('module', 'title', 'datetime', 'secret')
    ordering = ['datetime']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'moduleCode', 'academicYearStart', 'active')
    list_filter = ('title', 'moduleCode', 'academicYearStart', 'active')
    ordering = ['academicYearStart']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'studentId')
    list_filter = ('firstName', 'lastName', 'studentId')
    ordering = ['firstName']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'module')
    list_filter = ('student', 'module')
    ordering = ['module']

@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):
    list_display = ('professor', 'module')
    list_filter = ('professor', 'module')
    ordering = ['module']