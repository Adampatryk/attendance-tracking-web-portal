from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from lectures.models import *
from .serializers import *
from lectures.utils import *

from django.utils import timezone

#Get the attendances for a lecture
@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def api_lecture_attendance(request, lecture_id):

    if request.method=="GET":
        
        #If the user is a student, drop the request
        if (not request.user.usertypewrapper.is_lecturer):
            return Response({"Error":"Lecture attendance is only available for lecturers"}, status=status.HTTP_403_FORBIDDEN)

        #Check that this lecture exists
        try:
            lecture = models.Lecture.objects.get(id=lecture_id)
            studentsAttendanceRecords = utils.get_attendance_for_lecture(lecture)
            
        except Lecture.DoesNotExist:
            return Response({"Error":"The lecture does not exist"}, status=status.HTTP_404_NOT_FOUND)

        #Check that the user has access to the lecture
        if (lecture not in get_lectures_for_user(request.user)):
            return Response({"Error":"This user does not have access to this lecture"}, status=status.HTTP_403_FORBIDDEN)

        serializer = LectureAttendanceSerializer(studentsAttendanceRecords, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

#Get a list of all lecture for the current user lectures 
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def api_lecture(request):    
    #To retrieve list of lectures 
    if request.method == "GET":
        denormalized = False
        date = False
        module = False

        #Check if the lectures should be denormalized
        try:
            if (request.GET['denormalized'] == "true"):
                denormalized = True

        except Exception as e:
            denormalized = False

        #Check if there is a date specified
        try:
            requestDate = request.GET['date']

            #Check if date is in the correct format:
            try:
                date = datetime.strptime(requestDate, utils.DATE_FORMAT)
            except Exception:
                return Response({"Error":"The date needs to be in the format: " + utils.DATE_FORMAT}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            date = False

        

        #Check if the module is specified
        try:
            module = request.GET['module']

        except Exception as e:
            module = False

        #if module is specified then just get the lectures for the module
        if (module != False):

            #Check that the module exists
            try:
                module = models.Module.objects.get(id=module)
            except models.Module.DoesNotExist:
                return Response({"Error":"This module does not exist"}, status=status.HTTP_404_NOT_FOUND)

            #Check that the user has access to this module
            if (module not in get_modules_for_user(request.user)):
                return Response({"Error":"This account does not have access to this module"}, status=status.HTTP_403_FORBIDDEN)

            lectures = get_lectures_for_user(request.user, date=date, modules=[module])
        else:
            #Get all the lectures that the user has access to for the date specified (if any)
            lectures = get_lectures_for_user(request.user, date)


        #Choose serializer based on whether the data should be normalised or not
        if denormalized:
            serializer = LectureDenormalizedSerializer(lectures, many=True)
        else:
            serializer = LectureSerializer(lectures, many=True)

        return Response(serializer.data)
    
#Create a new lecture
@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def api_lecture_create(request):

    if request.method == "POST":

        user = request.user

        #If the user is a student, drop the request
        if user.usertypewrapper.is_lecturer == False:
            return Response({"Error":"This account is not authorized to create lectures"}, status=status.HTTP_401_UNAUTHORIZED)

        #Deserialize the data
        serializer = LectureSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            try:
                module_id = data['getModuleId']
                info = data['info']
                title = data['title']
                timestamp = data['datetime']

            except Exception: 
                return Response({"Error":"Required fields: 'module_id', 'info', 'title', 'timestamp'"}, status=status.HTTP_400_BAD_REQUEST)
            
            #Check that the module exists
            try:
                module = models.Module.objects.get(id=module_id)

            except Module.DoesNotExist:
                return Response({"Error":"Module does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            #Check that this user has access to this module
            if (module not in get_modules_for_user(user)):
                return Response({"Error":"Not authorized to create lectures for this module"}, status=status.HTTP_403_FORBIDDEN)

            print(timestamp)

            lecture = Lecture.objects.create(title=title, datetime=timestamp, module = module, info = info)
            print(lecture.datetime)
            serializer = LectureDenormalizedSerializer(lecture)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        #If invalid return with 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete a specific lecture
@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def api_lecture_delete(request):
    #To delete an existing lecture
    if request.method == "POST":
        user = request.user

        #If the user is a student, drop the request
        if user.usertypewrapper.is_lecturer == False:
            return Response({"Error":"This account is not authorized to delete lectures"}, status=status.HTTP_401_UNAUTHORIZED)

        #Deserialize the data
        serializer = LectureSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            try:
                module_id = data['getModuleId']
                lectureId = data['id']
            except Exception as e:
                return Response({"Error":"Required fields: 'module_id', 'id'"}, status=status.HTTP_400_BAD_REQUEST)


            #Check that this lecture exists and that the secret is correct
            try:
                module = models.Module.objects.get(id=module_id)

                #Check that this user has access to this module
                if (module not in get_modules_for_user(user)):
                    return Response({"Error":"Not authorized to delete lectures for this module"}, status=status.HTTP_403_FORBIDDEN)

                lecture = Lecture.objects.get(id=lectureId, module=module)
            except Lecture.DoesNotExist:
                return Response({"Error":"Lecture does not exist or is already deleted"}, status=status.HTTP_404_NOT_FOUND)

            #Delete the lecture
            lecture.delete()

            if lecture.id == None:
                lecture.id = -1

            serializer = LectureDenormalizedSerializer(lecture)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        #If invalid return with 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def api_module_list(request):
    modules = get_modules_for_user(request.user)

    if request.method == "GET":
        serializer = ModuleDetailSerializer(modules, many=True)
        return Response(serializer.data)

@api_view(['POST', ])
@permission_classes([IsAuthenticated,])
def api_attendance_record(request):

    # if request.method == "GET":
    #     #if the user is a lecturer, return all attendances for all lectures
    #     if (request.user.usertypewrapper.is_lecturer):
    #         attendances = Attendance.objects.all().filter(lecture__in = get_lectures_for_user(request.user))
    #     #if the user is a student return all attendance records for student
    #     else:
    #         attendances = Attendance.objects.filter(student = request.user)

    #     serializer = AttendanceDetailSerializer(attendances, many=True)
    #     return Response(serializer.data)

    if request.method == "POST":
        #If the request is from a lecturer account, do not proceed
        if request.user.usertypewrapper.is_lecturer:
            return Response({"Error":"Attendance not tracked for lecturers"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        #Deserialize the data
        serializer = AttendanceSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            lectureId = data['lecture']
            qrcode = data['qrcode']
            student = request.user
            deviceId = data['deviceId']
            timestamp = data['timestamp']

            #Verify that lecture exists
            try:
                lecture = Lecture.objects.get(id = lectureId)
            except Lecture.DoesNotExist:
                return Response({"Error":"Lecture not found"}, status=status.HTTP_404_NOT_FOUND)

    
            #Verify that the student is allowed to be at this lecture
            try: 
                attendance = Attendance.objects.get(student = student, lecture = lecture)
            except Attendance.DoesNotExist:
                print("Error: Student not assigned to this lecture")
                return Response({"Error":"Student not assigned to this lecture"}, status=status.HTTP_403_FORBIDDEN)
            
            #Check that this student hasn't already signed themselves into this lecture
            if (attendance.present == True):
                return Response({"Error":"Student already present"}, status=status.HTTP_208_ALREADY_REPORTED)
            
            #Verify that the timestamp is within the last 3 seconds
            if (not is_valid_timestamp(timestamp)):
                return Response({"Error":"This QR code is old"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            #Verify that user has scanned the QR code
            if (qrcode != get_qr_code(lecture.secret, timestamp-1)):
                if (qrcode != get_qr_code(lecture.secret, timestamp)):
                    if (qrcode != get_qr_code(lecture.secret, timestamp+1)):
                        return Response({"Error":"QR code not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            
            #Check that this device has not yet been used for this lecture
            if (Attendance.objects.filter(deviceId = deviceId, lecture = lecture).count() > 0):
                print ("Device already used")
                return Response({"Error":"Device already used"}, status=status.HTTP_409_CONFLICT)

            

            
            attendance.present = True
            attendance.deviceId = deviceId
            attendance.save()
            
            responseData = GetAttendanceSerializer(attendance)

            return Response(responseData.data, status=status.HTTP_202_ACCEPTED)

        #If invalid return with 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Get all the students for a specific lecture
@api_view(['GET', ])
@permission_classes([IsAuthenticated,])
def api_students_for_module(request, module_id):
    if request.method == "GET":

        #Check that the module exists
        try:
            module = models.Module.objects.get(id=module_id)
        except models.Module.DoesNotExist:
            return Response({"Error":"This module does not exist"}, status=status.HTTP_404_NOT_FOUND)

        #Check that the user has access to this module
        if (module not in get_modules_for_user(request.user)):
            return Response({"Error":"This account does not have access to this module"}, status=status.HTTP_403_FORBIDDEN)

        #Get the students for the module
        students = get_students_for_module(module)

        #If the user is a lecturer, attach the percentage attendace to each student
        if (request.user.usertypewrapper.is_lecturer):
            #For each student, get the percentage attendance for the module
            for student in students:
                student.attendance_for_module = get_attendance_percentage_for_student_for_module(student, module)

        serializer = UserSerializer(students, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

#Get all the lectures for a student for a module
@api_view(['GET', ])
@permission_classes([IsAuthenticated,])
def api_lectures_for_student_for_module(request, module_id, student_id):
    
    #Verify that the module exists
    try:
        module = models.Module.objects.get(id=module_id)
    except models.Module.DoesNotExist:
        return Response({"Error":"This module does not exist"}, status=status.HTTP_404_NOT_FOUND)

    #Verify that this user has access to this module
    if (module not in get_modules_for_user(request.user)):
        return Response({"Error":"This account does not have access to this module"}, status=status.HTTP_403_FORBIDDEN)

    #Verify that the user exists
    try:
        student = models.User.objects.get(id=student_id)
    except models.User.DoesNotExist:
        return Response({"Error":"This student does not exist"}, status=status.HTTP_404_NOT_FOUND)

    #Verify that the user is a student 
    if (student.usertypewrapper.is_lecturer == True):
        return Response({"Error":"The student_id is not the primary key of a student"}, status=status.HTTP_400_BAD_REQUEST)

    #Verify that the student is on the module
    if (student not in get_students_for_module(module)):
        return Response({"Error":"This student is not on the specified module"}, status=status.HTTP_400_BAD_REQUEST)

    #If the requesting user is not a lecturer, the id of the student_id must match request.user.id
    if (not request.user.usertypewrapper.is_lecturer) and student != request.user:

        #The requesting account is not a lecturers account so if the id of the requesting user 
        # and the student_id dont match then dont allow
        return Response({"Error":"This account cannot view this information"}, status=status.HTTP_403_FORBIDDEN)
        
    #If the user is a lecturer then at this point it is valid that they do teach the student:
        #They have access to the module
        #The student is on the module

    lecturesForStudentForModule = get_lectures_for_user(student, modules=[module])

    #Choose serializer based on whether the data should be normalised or not
    serializer = LectureSerializer(lecturesForStudentForModule, many=True)

    return Response(serializer.data)


# #Get the details for a lecture in JSON
# @api_view(['GET', ])
# @permission_classes([IsAuthenticated, ])
# def api_lecture_details(request, lecture_id):

#     #Make sure the lecture exists and that the user has access to it
#     try:
        
#         #Get the lecture
#         lecture = Lecture.objects.get(id = lecture_id)

#         #Get all modules
#         lectures_for_user = get_lectures_for_user(request.user)
#         #If the user does not teach this module, restrict access
#         if (lecture not in lectures_for_user):
#             return Response(status.HTTP_403_FORBIDDEN)

#     except Lecture.DoesNotExist: 
#         return Response(status.HTTP_404_NOT_FOUND)

#     if request.method == "GET": 

#         denormalized = False
#         try:
#             if (request.GET['denormalized'] == "true"):
#                 denormalized = True

#         except Exception as e:
#             denormalized = False

#         #If the requst comes from a student, make the secret null
#         if not request.user.usertypewrapper.is_lecturer:
#             lecture.secret = None

#         #Choose serializer based on whether the data should be normalised or not
#         if denormalized:
#             serializer = LectureDenormalizedSerializer(lecture)
#         else:
#             serializer = LectureSerializer(lecture)
#         return Response(serializer.data)

# @api_view(['GET', ])
# @permission_classes([IsAuthenticated, ])
# def api_module_details(request, module_id):
#     try:
#         #Get the module with id=module_id
#         module = Module.objects.get(id=module_id)
        
#         #Get all modules
#         modules_for_user = get_modules_for_user(request.user)
#         #If the user does not teach this module, restrict access
#         if (module not in modules_for_user):
#             return Response(status.HTTP_403_FORBIDDEN)

#     except Module.DoesNotExist:
#         return Response(status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         moduleSerializer = ModuleDetailSerializer(module)
#         return Response(moduleSerializer.data)