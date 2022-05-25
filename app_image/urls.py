from django.urls import path, include

from rest_framework import routers

from app_image.views import ImageViewSet

router = routers.DefaultRouter()
router.register('images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls))
]

app_name = 'app_image'
