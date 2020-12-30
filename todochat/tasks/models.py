from django.db import models
from django.contrib.auth.models import User
from app.models import Server
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    task_id = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_created_tasks')
    assigned_for = models.ManyToManyField(User, related_name='users_tasks')
    created     = models.DateTimeField(editable=False, default=timezone.now)
    modified    = models.DateTimeField(default=timezone.now)
    server = models.ForeignKey(Server, related_name='server_tasks', on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if not self.task_id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Task, self).save(*args, **kwargs)