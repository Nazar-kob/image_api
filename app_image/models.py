from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class ThumbnailSize(models.Model):
    size = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'{self.size}'


class ImageData(models.Model):
    image_url = models.URLField()
    original_image = models.ImageField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="image_data"
    )

    def __str__(self):
        return f"{self.image_url[-10:]}"


class NewImage(models.Model):
    new_image = models.ImageField()
    size = models.ForeignKey(
        ThumbnailSize,
        on_delete=models.CASCADE,
        related_name="image_size"
    )
    image_data = models.ForeignKey(
        ImageData,
        on_delete=models.CASCADE,
        related_name="images"
    )

    def __str__(self):
        return f"{self.new_image}"


class Tier(models.Model):
    name = models.CharField(max_length=255)
    is_original_link = models.BooleanField(default="False")
    thumbnail_sizes = models.ManyToManyField(
        ThumbnailSize,
        related_name="tier"
    )

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, default="1")

    def __str__(self):
        return f"{self.username}"
