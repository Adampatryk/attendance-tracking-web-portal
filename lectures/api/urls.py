from django.urls import path

from lectures.api import views

app_name = 'api_lectures'

urlpatterns = [
    path('', views.api_lecture_list, name='list'),
    path('<int:lecture_id>', views.api_lecture_details, name='details'),
    path('modules/', views.api_module_list, name='modules_list'),
    path('modules/<int:module_id>', views.api_module_details, name='module_details'),
    path('students/', views.api_student_list, name='student_list'),
    path('students/<int:student_id>', views.api_student_details, name='student_details'),
]