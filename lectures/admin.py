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
    list_display = ('title', 'professorId', 'moduleCode', 'academicYearStart', 'active')
    list_filter = ('title', 'professorId', 'moduleCode', 'academicYearStart', 'active')
    ordering = ['academicYearStart']