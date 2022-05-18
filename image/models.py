from django.contrib.auth.models import AbstractUser
from django.db import models


class Tier(models.Model):
    name = models.CharField(max_length=255)
    max_thumbnail_size = models.PositiveIntegerField()
    access_original_link = models.BooleanField(default="False")

    def __str__(self):
        return f"{self.name}"






class User(AbstractUser):
    # build_tiers = [
    #     ("Basic", Tier("Basic", 200)),
    #     ("Enterprise", Tier("Enterprise", 400))
    # ]

    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.username}"


class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="img/")
    thumbnail_size = models.PositiveIntegerField()
    original_link = models.CharField(max_length=355, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
