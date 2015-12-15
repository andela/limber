from django.conf.urls import include, url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from app import viewsets


router = routers.DefaultRouter()

router.register(r'org', viewsets.OrgSignUpViewSet, 'org')
router.register(r'user', viewsets.UserSignUpViewSet, 'user')
router.register(r'project', viewsets.ProjectViewSet, 'project')
router.register(r'team', viewsets.TeamMemberViewSet)


urlpatterns= [
    url(r'^', include(router.urls))
]



urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]