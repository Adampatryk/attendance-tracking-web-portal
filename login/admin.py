from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from login.models import UserTypeWrapper

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = UserTypeWrapper
    can_delete = False
    verbose_name_plural = 'usertypewrapper'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)
    list_display = ('username', 'id', 'password', 'is_lecturer', 'last_login', 'date_joined')
    list_filter = ('last_login', 'date_joined')
    ordering = ['id']
    
    def is_lecturer(self, obj):
        return obj.usertypewrapper.is_lecturer

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)