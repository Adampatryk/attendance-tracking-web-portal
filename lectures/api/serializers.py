from rest_framework import serializers
from lectures.models import * 

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'module', 'title', 'datetime', 'secret']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'professor', 'moduleCode', 'academicYearStart', 'active']