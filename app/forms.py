from django import forms
from .models import UploadedImage, UploadedVideo

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ("image",)

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo
        fields = ("video",)