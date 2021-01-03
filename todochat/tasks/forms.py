from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from tasks.models import Task
from django.contrib.auth.models import User

class TaskDescriptionForm(forms.Form):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        fields = ['description']

class TaskUpdateForm(forms.ModelForm):
    title = forms.CharField()
    assigned_for = forms.ModelMultipleChoiceField(queryset=None, 
    widget=forms.CheckboxSelectMultiple)
    description = forms.CharField(widget=CKEditorUploadingWidget())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_for'].queryset = User.objects.filter(server = self.instance.server)

    class Meta:
        model = Task
        fields = ['title', 'assigned_for', 'description']
