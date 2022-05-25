from rest_framework import viewsets

from app_image.models import ImageData
from app_image.serializers import ImageDataSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageData.objects.all()
    serializer_class = ImageDataSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)
