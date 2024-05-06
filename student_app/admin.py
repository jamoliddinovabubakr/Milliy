from django.contrib import admin
from .models import Student, Result

from django.contrib.auth.models import Group, User

admin.site.unregister(User)
admin.site.unregister(Group)


# admin.site.register(Student)
admin.site.register(Result)
