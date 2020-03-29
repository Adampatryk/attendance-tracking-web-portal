from rest_framework import serializers
from lectures.models import * 
from lectures.utils import *

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'module', 'title', 'datetime', 'secret']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'moduleCode', 'academicYearStart', 'active']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'firstName', 'lastName', 'studentId']

class ModuleDetailSerializer(serializers.ModelSerializer):

    students = serializers.SerializerMethodField('get_students_for_module')
    professors = serializers.SerializerMethodField('get_professors_for_module')

    class Meta:
        model = Module
        fields = ['id', 'title', 'moduleCode', 'academicYearStart', 'active', 'students', 'professors']

    def get_students_for_module(self, module):
        students = get_students_for_module(module)
        return StudentSerializer(students, many=True).data
    
    def get_professors_for_module(self, module):
        professors = get_professors_for_module(module)
        return UserSerializer(professors, many=True).data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined']

class StudentDetailSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField('get_modules_for_student')

    class Meta:
        model = Student
        fields = ['id', 'firstName', 'lastName', 'studentId', 'modules']
    
    def get_modules_for_student(self, student):
        modules = get_modules_for_student(student)
        return ModuleSerializer(modules, many=True).data
