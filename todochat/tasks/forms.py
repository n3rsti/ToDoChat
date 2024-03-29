from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from tasks.models import Task, TaskComment
from app.models import Server


class TaskDescriptionForm(forms.Form):
    description = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    server = forms.ChoiceField(choices=[
        (server.id, server.name) for server in Server.objects.all()
    ], required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskDescriptionForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['server'].choices = [(server.id, server.name) for server in
                                             Server.objects.filter(users=user)]

    class Meta:
        fields = ['description', 'server']


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
    content = forms.CharField(widget=CKEditorUploadingWidget(), min_length=1, label="")

    class Meta:
        model = TaskComment
        fields = ['content']


class TaskFilterForm(forms.Form):
    title__contains = forms.CharField(required=False)
    status = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[
        ("open", "Open"),
        ("approved", "Approved"),
        ("submitted_for_review", "Submitted for review"),
        ("need_more_work", "Need more work"),
    ], required=False)
    server = forms.ChoiceField(choices=[
        (server.id, server.name) for server in Server.objects.all()
    ], required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['server'].choices = [('All', 'All')] + [(server.id, server.name) for server in
                                                                Server.objects.filter(users=user)]
        self.fields['title__contains'].label = "Title"

    class Meta:
        fields = ['title__contains', 'status']


class TaskSortForm(forms.Form):
    order = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ("-created", "Created: Recent first"),
        ("created", "Created: Recent last"),
        ("-deadline", "Close to deadline"),
        ("deadline", "Far from deadline"),
    ], required=False)
