from rest_framework import serializers
from lectures.models import * 
from lectures.utils import *

class LectureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    secret = serializers.CharField(required=False, max_length=64)
    title = serializers.CharField(required=False, max_length=50)
    info = serializers.CharField(required=False, max_length=256)
    module_id = serializers.IntegerField(source='getModuleId')
    datetime = serializers.DateTimeField(required=False)
    present = serializers.ReadOnlyField(source='getPresent')

    class Meta:
        model = Lecture
        fields = ['id', 'module_id', 'title', 'info', 'datetime', 'present', 'secret']

class LectureDenormalizedSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField('get_module_detail')
    present = serializers.ReadOnlyField(source='getPresent')

    class Meta:
        model = Lecture
        fields = ['id', 'module', 'title', 'info', 'datetime', 'present', 'secret']

    def get_module_detail(self, lecture):
        return ModuleDetailSerializer(lecture.module).data


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'moduleCode',  'weight', 'info', 'academicYearStart', 'active']

class ModuleDetailSerializer(serializers.ModelSerializer):

    students = serializers.SerializerMethodField('get_students_for_module')
    professors = serializers.SerializerMethodField('get_professors_for_module')

    class Meta:
        model = Module
        fields = ['id', 'title', 'moduleCode', 'weight', 'info', 'academicYearStart', 'active', 'students', 'professors']

    def get_students_for_module(self, module):
        students = get_students_for_module(module)
        return UserSerializer(students, many=True).data
    
    def get_professors_for_module(self, module):
        professors = get_professors_for_module(module)
        return UserSerializer(professors, many=True).data

class UserSerializer(serializers.Serializer):
    is_lecturer = serializers.SerializerMethodField('get_is_lecturer')
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    date_joined = serializers.DateTimeField()
    attendance_for_module = serializers.DecimalField(max_digits=3, decimal_places=2, required=False)

    # class Meta:
    #     model = User
    #     fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'is_lecturer', 'attendance_for_module']

    def get_is_lecturer(self, user):
        try:
            return models.User.objects.get(id=user.id).usertypewrapper.is_lecturer
        except models.User.DoesNotExist:
            return False

    

class AttendanceSerializer(serializers.Serializer):
    lecture = serializers.IntegerField()
    qrcode = serializers.CharField(max_length=64)
    deviceId = serializers.CharField(max_length=16)
    timestamp = serializers.IntegerField()


class GetAttendanceSerializer(serializers.ModelSerializer):
    studentId = serializers.SerializerMethodField('get_student_id')
    class Meta:
        model = Attendance
        fields = ['lecture', 'deviceId', 'studentId', 'present', ]

    def get_student_id(self, attendance):
        return attendance.student.id

class AttendanceDetailSerializer(serializers.ModelSerializer):
    lecture = serializers.SerializerMethodField('get_lecture_for_attendance')
    student = serializers.SerializerMethodField('get_student_for_attendance')

    class Meta:
        model = Attendance
        fields = ['lecture', 'deviceId', 'timestamp', 'student', 'present']

    def get_lecture_for_attendance(self, attendance):
        lecture = Lecture.objects.get(id=attendance.lecture.id)
        return LectureSerializer(lecture).data

    def get_student_for_attendance(self, attendance):
        student = User.objects.get(id=attendance.student.id)
        return UserSerializer(student).data

class LectureAttendanceSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField('get_student_for_attendance')
    date = serializers.ReadOnlyField(source='timestamp')
    
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'present']

    def get_student_for_attendance(self, attendance):
        student = User.objects.get(id=attendance.student.id)
        return UserSerializer(student).data
