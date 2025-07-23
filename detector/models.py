from django.db import models

class UploadedImage(models.Model):
    image= models.ImageField(upload_to='images/')
    processed_image =models.ImageField(upload_to='processed_images/', null= True, blank=True)
    uploaded_at =models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"Image uploaded at {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
