from django.contrib import admin
from .models import Profile, UserInvitation

admin.site.register(Profile)
admin.site.register(UserInvitation)