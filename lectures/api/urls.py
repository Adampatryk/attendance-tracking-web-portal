from django.urls import path

from lectures.api import views

app_name = 'api_lectures'

urlpatterns = [
    path('', views.api_lecture, name='lectures'),
    path('create/', views.api_lecture_create, name='lecture_create'),
    path('delete/', views.api_lecture_delete, name='lecture_delete'),
    #path('<int:lecture_id>', views.api_lecture_details, name='details'),
    path('<int:lecture_id>/attendance/', views.api_lecture_attendance, name='lecture_attendance'),
    path('modules/', views.api_module_list, name='modules_list'),
    #path('modules/<int:module_id>', views.api_module_details, name='module_details'),
    path('modules/<int:module_id>/students/', views.api_students_for_module, name='students_for_module'),
    path('modules/<int:module_id>/students/<int:student_id>/lectures/', views.api_lectures_for_student_for_module, name='lectures_for_student_for_module'),
    path('attendance/', views.api_attendance_record, name='attendance_records'),
]