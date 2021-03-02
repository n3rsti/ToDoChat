from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from tasks.models import Task, TaskComment
from app.models import Server


class TaskDescriptionForm(forms.Form):
    description = forms.CharField(widget=CKEditorUploadingWidget(
        extra_plugins=['easyimage'],
        external_plugin_resources=[(
            'easyimage',
            '/static/ckeditor/ckeditor/easyimage/',
            'plugin.js'
        )]
        )
    )

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
    description = forms.CharField(widget=CKEditorUploadingWidget(
        extra_plugins=['easyimage'],
        external_plugin_resources=[(
            'easyimage',
            '/static/ckeditor/ckeditor/easyimage/',
            'plugin.js'
        )]
    )
    )

    class Meta:
        model = Task
        fields = ['title', 'description']


class TaskCommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(
        config_name="comment",
        extra_plugins=['easyimage'],
        external_plugin_resources=[(
            'easyimage',
            '/static/ckeditor/ckeditor/easyimage/',
            'plugin.js'
        )]), min_length=1, label="")

    class Meta:
        model = TaskComment
        fields = ['content']


class TaskFilterForm(forms.Form):
    title = forms.CharField(required=False)
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

    class Meta:
        fields = ['title', 'status']


class TaskSortForm(forms.Form):
    order = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ("-created", "Created: Recent first"),
        ("created", "Created: Recent last"),
        ("-deadline", "Close to deadline"),
        ("deadline", "Far from deadline"),
    ], required=False)
