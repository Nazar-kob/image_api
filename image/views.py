from rest_framework import viewsets, mixins

from image.models import Image
from image.serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = self.queryset
        if str(self.request.user.tier) == "Basic":
            queryset = Image.objects.filter(thumbnail_size=200)
        return queryset