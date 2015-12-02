from django.conf.urls import include, url
from rest_framework import routers
from app.serializers import profile_serializer


router = routers.DefaultRouter()

router.register(r'org_create', profile_serializer.OrgSignUpViewSet, 'org')
router.register(r'login', profile_serializer.LoginViewSet)
router.register(r'user_signup', profile_serializer.UserSignUpViewSet, 'user')

urlpatterns= [
    url(r'^', include(router.urls))
]
