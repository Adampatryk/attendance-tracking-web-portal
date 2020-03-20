from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from lectures.models import *
from .serializers import *

@api_view(['GET', ])
def api_lecture_details(request, lecture_id):
    lecture = Lecture.objects.get(id = lecture_id)

    if request.method == "GET":
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)