from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class TaskDescriptionForm(forms.Form):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        fields = ['description']
