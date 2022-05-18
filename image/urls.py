from django.urls import path, include

from rest_framework import routers

from image.views import ImageViewSet

router = routers.DefaultRouter()
router.register('images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls))
]

app_name = 'image'
