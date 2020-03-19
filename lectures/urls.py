from django.urls import path
from . import views

app_name = "lectures"

urlpatterns = [
    path('', views.lecture_list, name='list'),
    path('create', views.lecture_create, name='create'),
    path('<int:id>', views.lecture_details, name='details'),
    path('qr-code/<int:id>', views.lecture_qr_code, name='qr-code'),
    path('delete/<int:id>', views.lecture_delete, name='delete'),
    path('modules', views.modules_list, name='list_modules'),
    path('modules/<int:id>', views.module_details, name='module_details')
]