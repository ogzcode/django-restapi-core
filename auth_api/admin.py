from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


def get_user_groups(obj):
    if hasattr(obj, 'user'):
        return ', '.join([group.name for group in obj.user.groups.all()])
    else:
        return ', '.join([group.name for group in obj.groups.all()])


get_user_groups.short_description = 'Gruplar'


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'is_staff', get_user_groups)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
