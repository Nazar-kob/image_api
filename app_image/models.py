from django.contrib.auth.models import AbstractUser
from django.db import models


class Tier(models.Model):
    name = models.CharField(max_length=255)
    max_thumbnail_size = models.PositiveIntegerField()
    is_original_link = models.BooleanField(default="False")
    is_time_exist = models.BooleanField(default="False")

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, default="1")

    def __str__(self):
        return f"{self.username}"


class OriginalLink(models.Model):
    original_link = models.CharField(max_length=355, blank=True, null=True)


class ImageData(models.Model):
    image = models.ImageField(upload_to="img/")
    image_size = models.PositiveIntegerField()
    image_original_link = models.OneToOneField(OriginalLink, on_delete=models.CASCADE, related_name="image")

