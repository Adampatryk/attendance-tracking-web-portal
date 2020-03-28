from django.urls import path
from . import views

app_name = "lectures"

urlpatterns = [
    path('', views.lecture_list, name='list'),
    path('create', views.lecture_create, name='create'),
    path('<int:lecture_id>', views.lecture_details, name='details'),
    path('qr-code/<int:lecture_id>', views.lecture_qr_code, name='qr-code'),
    path('delete/<int:lecture_id>', views.lecture_delete, name='delete'),
    path('modules', views.module_list, name='modules_list'),
    path('modules/<int:module_id>', views.module_details, name='module_details'),
    path('students', views.student_list, name='students_list'),
    path('students/<int:student_id>', views.student_details, name='student_details')
]