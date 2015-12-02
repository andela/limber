from django.conf.urls import include, url
from rest_framework import routers
from app.serializers import profile_serializer


router = routers.DefaultRouter()

router.register(r'org', profile_serializer.OrgSignUpViewSet, 'org')
router.register(r'user', profile_serializer.UserSignUpViewSet, 'user')

urlpatterns= [
    url(r'^', include(router.urls))
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]