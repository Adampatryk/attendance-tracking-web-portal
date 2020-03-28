from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from lectures.models import *
from .serializers import *
from lectures.utils import *

#Get the details for a lecture in JSON
@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def api_lecture_details(request, lecture_id):

    #Make sure the lecture exists and that the user has access to it
    try:
        #Get the lecture
        lecture = Lecture.objects.get(id = lecture_id)

        #If the user is not the teacher of this module, forbid access
        if (lecture.module.professor != request.user):
            return Response(status.HTTP_403_FORBIDDEN)

    except Lecture.DoesNotExist: 
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == "GET": 
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)

#Get a list of lectures in JSON
@api_view(['GET',])
@permission_classes([IsAuthenticated, ])
def api_lecture_list(request):     
    
    #Get all the lectures that the user has access to
    users_lectures = get_lectures_for_user(request.user.id)

    if request.method == "GET":
        serializer = LectureSerializer(users_lectures, many=True)
        return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def api_module_details(request, module_id):
    try:
        #Get the module with id=module_id
        module = Module.objects.get(id=module_id)
        
        #If the user is not the professor for this module, forbid access
        if (module.professor != request.user):
            return Response(status.HTTP_403_FORBIDDEN)

    except Module.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        moduleSerializer = ModuleDetailSerializer(module)
        return Response(moduleSerializer.data)

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def api_module_list(request):
    modules = get_modules_for_user(request.user)

    if request.method == "GET":
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def api_student_list(request):

    students = get_students_for_user(request.user)

    if request.method == "GET":
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def api_student_details(request, student_id):
    #Get the student, 404 if not found
    try:
        student = Student.objects.get(id=student_id)

        #Check if this student is taught by this user
        students_for_user = get_students_for_user(request.user)

        #If student not taught by user, forbid access
        if student not in students_for_user:
            return Response(status.HTTP_403_FORBIDDEN)

    except Student.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    # modules = get_modules_for_student(student)

    # allocations = Allocation.objects.all().filter(student=student)

    if request.method == "GET":
        serializer = StudentDetailSerializer(student)
        return Response(serializer.data)