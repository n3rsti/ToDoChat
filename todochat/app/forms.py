from django import forms
from app.models import Server

class ServerUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-light'}))

    class Meta:
        model = Server
        fields = ['name', 'image']

    def __init__(self, *args, **kwargs):
        super(ServerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class ServerCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-light'}))

    class Meta:
        model = Server
        fields = ['name', 'image']

    def __init__(self, *args, **kwargs):
        super(ServerCreateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False