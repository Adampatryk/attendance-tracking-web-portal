from rest_framework import serializers
from lectures.models import * 
from lectures.utils import *

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'module', 'title', 'datetime', 'secret']

class LectureDenormalizedSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField('get_module_detail')
    class Meta:
        model = Lecture
        fields = ['id', 'module', 'title', 'datetime', 'secret']

    def get_module_detail(self, lecture):
        return ModuleDetailSerializer(lecture.module).data


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'moduleCode', 'academicYearStart', 'active']

class ModuleDetailSerializer(serializers.ModelSerializer):

    students = serializers.SerializerMethodField('get_students_for_module')
    professors = serializers.SerializerMethodField('get_professors_for_module')

    class Meta:
        model = Module
        fields = ['id', 'title', 'moduleCode', 'academicYearStart', 'active', 'students', 'professors']

    def get_students_for_module(self, module):
        students = get_students_for_module(module)
        return UserSerializer(students, many=True).data
    
    def get_professors_for_module(self, module):
        professors = get_professors_for_module(module)
        return UserSerializer(professors, many=True).data

class UserSerializer(serializers.ModelSerializer):
    is_lecturer = serializers.SerializerMethodField('get_is_lecturer')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'is_lecturer']

    def get_is_lecturer(self, user):
        return user.usertypewrapper.is_lecturer
