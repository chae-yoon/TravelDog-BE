from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # 파일 업로드 경로 설정
    def get_profile_image_upload_path(instance, filename):
        return f'profile_images/{instance.username}/{filename}'
    
    phone_number = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to=get_profile_image_upload_path, null=True, blank=True)