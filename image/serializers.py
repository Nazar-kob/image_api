from rest_framework import serializers

from image.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #
    #     print(representation.get('thumbnail_size'))
    #
    #     return representation
