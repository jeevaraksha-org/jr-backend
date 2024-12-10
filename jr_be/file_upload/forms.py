from django import forms
from core.models import DocumentUpload


class Upload_Form(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = [
            'description',
            'document',
        ]
