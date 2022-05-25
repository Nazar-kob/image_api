from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Tier(models.Model):
    name = models.CharField(max_length=255)
    is_thumbnail_200 = models.BooleanField(default="False")
    is_thumbnail_400 = models.BooleanField(default="False")
    is_original_link = models.BooleanField(default="False")
    is_time_exist = models.BooleanField(default="False")

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, default="1")

    def __str__(self):
        return f"{self.username}"


class ImageData(models.Model):
    image_url = models.URLField()
    origin_image_url = models.ImageField()
    thumbnail_200 = models.ImageField()
    thumbnail_400 = models.ImageField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
