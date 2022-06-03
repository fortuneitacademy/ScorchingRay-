from dataclasses import fields
from django import forms
from .models import Student,UploadModel

class UploadFileForm(forms.ModelForm):
    file = UploadModel()