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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_created_tasks')
    assigned_for = models.ManyToManyField(User, related_name='users_tasks')
    created     = models.DateTimeField(editable=False, default=timezone.now)
    modified    = models.DateTimeField(default=timezone.now)
    server = models.ForeignKey(Server, related_name='server_tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="open")

    def save(self, *args, **kwargs):
        if not self.task_id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.server.name} #{self.task_id}'
    
    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'server_id': self.server.id, 'id': self.id})



class TaskComment(models.Model):
    task_type = models.CharField(max_length=20, default="comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_task_comments')
    created     = models.DateTimeField(editable=False, default=timezone.now)
    modified    = models.DateTimeField(default=timezone.now)
    content = RichTextUploadingField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_comments")