from django import forms
from desafio.models import Upload

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('arquivo',)

        widgets = {
            'arquivo': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Arquivo:'}),
        }