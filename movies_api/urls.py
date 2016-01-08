from django.conf.urls import url, include

from rest_framework import routers
from .viewsets import MovieViewSet

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
]
