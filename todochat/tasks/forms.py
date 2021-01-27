from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from tasks.models import Task, TaskComment
from django.contrib.auth.models import User
from app.models import Server

class TaskDescriptionForm(forms.Form):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        fields = ['description']

class TaskUpdateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'title',
        'id': 'title',
        'class': 'form-control',
        'placeholder': 'For example: make an app',
        'required': 'true'
    }))
    description = forms.CharField(widget=CKEditorUploadingWidget())


    class Meta:
        model = Task
        fields = ['title', 'description']


class TaskCommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name="comment"), min_length=1, label="")

    class Meta:
        model = TaskComment
        fields = ['content']