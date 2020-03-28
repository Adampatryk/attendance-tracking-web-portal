from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from lectures.models import *
from .serializers import *

@api_view(['GET', ])
def api_lecture_details(request, lecture_id):
    try:
        lecture = Lecture.objects.get(id = lecture_id)
    except Lecture.DoesNotExist: 
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == "GET": 
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)

@api_view(['GET',])
def api_lecture_list(request):     
    lectures = Lecture.objects.all()

    if request.method == "GET":
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

@api_view(['GET', ])
def api_module_details(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ModuleSerializer(module)
        return Response(serializer.data)

@api_view(['GET', ])
def api_module_list(request):
    modules = Module.objects.all()

    if request.method == "GET":
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)
    