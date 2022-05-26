import os

from PIL import Image
from django.db import transaction
from rest_framework import serializers
from urllib.request import urlopen
import urllib.request
import uuid

from app_image.models import ImageData, NewImage


class NewImageSerializer(serializers.ModelSerializer):
    size = serializers.CharField(read_only=True)
    original_url = serializers.ImageField(
        source="image_data.original_image",
        read_only=True
    )

    class Meta:
        model = NewImage
        fields = ("new_image", "size", "original_url")


class ImageDataListSerializer(serializers.ModelSerializer):
    images = NewImageSerializer(many=True, read_only=True)

    class Meta:
        model = ImageData
        fields = ("images", "image_url")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        get_user_tier = instance.user.tier
        for image in representation["images"]:
            if get_user_tier.is_original_link:
                representation["original_url"] = image["original_url"]
            representation[f"thumbnail_{image['size']}"] = image["new_image"]

        del representation["images"]
        del representation["image_url"]

        return representation

    def create(self, validated_data):

        try:
            with transaction.atomic():
                image_url = validated_data.get("image_url")
                user = self.context["request"].user

                image_url = self.is_valid_url_and_user(image_url, user)

                original_image_name = f"original_img/{str(uuid.uuid4())}.jpg"
                urllib.request.urlretrieve(image_url, original_image_name)

                image_data_obj = ImageData.objects.create(
                    image_url=image_url,
                    original_image=original_image_name,
                    user=user
                )

                self.create_another_thumbnail_img(image_data_obj, user)
        except Exception as error:
            if error.args:
                raise serializers.ValidationError(f"{error.args[0]}")
            raise serializers.ValidationError(
                'Something is wrong with your "jpg" image URL.'
            )

        return image_data_obj

    @staticmethod
    def is_valid_url_and_user(url, user):
        image_formats = ("image/jpeg",)
        site = urlopen(url)
        meta = site.info()
        if meta["content-type"] not in image_formats:
            raise serializers.ValidationError(
                'This URL is not suitable for "jpg" image requests'
            )

        if str(user) == "AnonymousUser":
            raise serializers.ValidationError(
                "You must first sign in before submitting a URL"
            )

        return url

    @staticmethod
    def create_another_thumbnail_img(image_data_obj, user):
        for thumbnail_sizes in user.tier.thumbnail_sizes.all():

            with Image.open(image_data_obj.original_image) as original_img:
                new_size = int(thumbnail_sizes.size)
                new_dir = f"new_img_{thumbnail_sizes.size}/"

                if not os.path.isdir(new_dir):
                    os.mkdir(new_dir)

                new_name_image = str(
                    image_data_obj.original_image
                ).replace(
                    "original_img/", new_dir
                ).replace(
                    ".jpg", f"_{new_size}.jpg")

                original_img.thumbnail((new_size, new_size))
                original_img.save(new_name_image)

            NewImage.objects.create(
                new_image=new_name_image,
                size=thumbnail_sizes,
                image_data=image_data_obj
            )
