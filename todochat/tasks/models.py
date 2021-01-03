from django.db import models
from django.contrib.auth.models import User
from app.models import Server
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Task(models.Model):
    task_id = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    description = RichTextUploadingField(blank=True, null=True)
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
    
    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'server_id': self.server.id, 'id': self.id})