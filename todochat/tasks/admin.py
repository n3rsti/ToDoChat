from django.contrib import admin
from .models import Task, TaskComment

admin.site.register(Task)
admin.site.register(TaskComment)
