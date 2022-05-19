from rest_framework import serializers

from app_image.models import OriginalLink


class ImageSerializerList(serializers.ModelSerializer):
    class Meta:
        model = OriginalLink
        fields = "__all__"

    def create(self, validated_data):
        url = validated_data.get("original_link")

        return OriginalLink.objects.create(**validated_data)
