from django.contrib import admin
from .models import Profile, UserInvitation, UsersChat, UsersMessage

admin.site.register(Profile)
admin.site.register(UserInvitation)
admin.site.register(UsersChat)
admin.site.register(UsersMessage)
