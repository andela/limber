from django.conf.urls import include, url
from rest_framework import routers
from app.serializers import profile_serializer


router = routers.DefaultRouter()
router.register(r'users', profile_serializer.ProfileViewSet)

urlpatterns= [
    url(r'^', include(router.urls))
]
