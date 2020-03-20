from rest_framework import serializers
from lectures.models import * 

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['module', 'title', 'datetime', 'secret']