


from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UploadedVideo(models.Model):
    video = models.FileField(upload_to="videos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Plain text (not secure)