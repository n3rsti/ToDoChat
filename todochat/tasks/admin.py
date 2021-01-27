from django.contrib import admin
from .models import Task, TaskComment, TaskStatusChange

admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TaskStatusChange)
