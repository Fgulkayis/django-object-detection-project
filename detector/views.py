from django.shortcuts import render, redirect
from django.conf import settings 
from django.core.files.storage import FileSystemStorage
import os
import cv2
import numpy as np
from .forms import ImageUploadForm
from .models import UploadedImage 
from .yolo_detector import ObjectDetector

detector_model = ObjectDetector()

def upload_iamge(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image_instance =form.save(commit=False)
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        
            image_name = uploaded_image_instance.image.name 
            original_image_path_on_disk =os.path.join(fs.location, uploaded_image_instance.image.name)

            uploaded_image_instance.save()

            image_full_path = uploaded_image_instance.image.path

            try:
               annotated_image_np = detector_model.detect_objects(image_full_path)

               original_file_name, file_extension = os.path.splitext(os.path.basename(image_name))

               processed_image_name = f"processed_{original_file_name}{file_extension}"

               processed_image_full_path = os.path.join(settings.MEDIA_ROOT,'processed_images', processed_image_name)

               os.makedirs(os.path.dirname(processed_image_full_path), exist_ok=True)

               cv2.imwrite(processed_image_full_path, annotated_image_np)

               uploaded_image_instance.processed_image.name = os.path.join('processed_images', processed_image_name)

               uploaded_image_instance.save()
               
               return render(request, 'detector/result.html', {'uploaded_image': uploaded_image_instance})
            
            except FileNotFoundError as e:
                return render(request, 'detector/error.html', {'error_message': f"Dosya hatası: {e}"})
            except Exception as e:
                 return render(request, 'detector/error.html', {'error_message': f"Nesne tanımlama sırasında bir hata oluştu: {e}"})
        else:
            form = ImageUploadForm()
            return render(request, 'detector/upload.html', {'from': form})