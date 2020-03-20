from django.urls import path

from lectures.api import views

app_name = 'lectures'

urlpatterns = [
    path('<int:lecture_id>', views.api_lecture_details, name='details'),
]