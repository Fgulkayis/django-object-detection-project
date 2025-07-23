from django import forms 
from .models import UploadedImage

class ImageUploadform(forms.ModelForm):
    class Meta:
        Model = UploadedImage
        fields = ['image']