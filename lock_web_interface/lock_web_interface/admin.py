from django.contrib import admin

from lock_web_interface.models import LoginEntry, MyUser

admin.site.register(MyUser)
admin.site.register(LoginEntry)