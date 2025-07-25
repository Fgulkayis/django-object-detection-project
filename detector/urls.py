from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'detector'

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
