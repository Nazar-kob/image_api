from rest_framework import viewsets, mixins

from app_image.models import ImageData
from app_image.serializers import ImageDataListSerializer


class ImageViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = ImageData.objects.all()
    serializer_class = ImageDataListSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)
