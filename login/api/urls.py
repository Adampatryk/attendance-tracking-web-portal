from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = "api_login"

urlpatterns = [
    path('', obtain_auth_token, name="login"),
]