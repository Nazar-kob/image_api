from PIL import Image
from django.db import transaction
from rest_framework import serializers
from urllib.request import urlopen
import urllib.request
import uuid

from app_image.models import ImageData


class ImageDataSerializer(serializers.ModelSerializer):
    thumbnail_200_link = serializers.ImageField(source="thumbnail_200", read_only=True)
    thumbnail_400_link = serializers.ImageField(source="thumbnail_400", read_only=True)
    origin_url = serializers.ImageField(source="origin_image_url", read_only=True)

    class Meta:
        model = ImageData
        fields = ("image_url", "thumbnail_200_link", "thumbnail_400_link", "origin_url")

    @staticmethod
    def is_valid_url_and_user(url, user):
        image_formats = ("image/png", "image/jpeg")
        site = urlopen(url)
        meta = site.info()
        if meta["content-type"] not in image_formats:
            raise serializers.ValidationError("is not valid url")

        if str(user) == "AnonymousUser":
            raise serializers.ValidationError("you should be sign in")

        return url

    @staticmethod
    def create_another_thumbnail(file_name, file_size):
        with Image.open(file_name) as img:
            file_place = f"image_size_{file_size}/{str(uuid.uuid4())}_{file_size}.jpg"
            img.thumbnail((file_size, file_size))
            img.save(file_place)

        return file_place

    def create(self, validated_data):
        with transaction.atomic():
            try:
                image_url = validated_data.get("image_url")
                user = self.context['request'].user

                image_url = self.is_valid_url_and_user(image_url, user)

                original_image_name = f"img/{str(uuid.uuid4())}.jpg"
                urllib.request.urlretrieve(image_url, original_image_name)

                img_object = ImageData.objects.create(
                    image_url=image_url,
                    origin_image_url=original_image_name,
                    thumbnail_200=self.create_another_thumbnail(original_image_name, 200),
                    thumbnail_400=self.create_another_thumbnail(original_image_name, 400),
                    user=user
                )



            except serializers.ValidationError as error:
                raise serializers.ValidationError(f"{error.args[0]}")
            except Exception:
                raise serializers.ValidationError(f"wrong url")

            return img_object

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        get_user_tier = instance.user.tier
        if not get_user_tier.is_original_link:
            del representation["origin_url"]
        if not get_user_tier.is_thumbnail_200:
            del representation["thumbnail_200_link"]
        if not get_user_tier.is_thumbnail_400:
            del representation["thumbnail_400_link"]
        del representation["image_url"]
        return representation
