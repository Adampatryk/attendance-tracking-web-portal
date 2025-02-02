from django.contrib import admin
from .models import *
from login.models import *

# Register your models here.
@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'module', 'title', 'info', 'datetime', 'secret')
    list_filter = ('module', 'datetime')
    ordering = ['datetime']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'weight', 'moduleCode', 'info', 'academicYearStart', 'active')
    list_filter = ('moduleCode', 'academicYearStart', 'active')
    ordering = ['academicYearStart']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'module')
    list_filter = ('student', 'module')
    ordering = ['module']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(usertypewrapper__is_lecturer=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):
    list_display = ('professor', 'module')
    list_filter = ('professor', 'module')
    ordering = ['module']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'student', 'present', 'timestamp', 'deviceId')
    list_filter = ('lecture', 'student', 'present', 'timestamp', 'deviceId')
    ordering = ['timestamp']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(usertypewrapper__is_lecturer=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)