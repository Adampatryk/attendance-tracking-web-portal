from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = "api_login"

urlpatterns = [
    path('', views.CustomAuthToken.as_view(), name="login"),
]