from django.conf.urls import include, url
from rest_framework import routers
from app import viewsets
from app import views

router = routers.DefaultRouter()

router.register(r'org', viewsets.OrgSignUpViewSet, 'org')
router.register(r'user', viewsets.UserSignUpViewSet, 'user')
router.register(r'member', viewsets.MemberViewSet, 'member')
router.register(r'project', viewsets.ProjectViewSet, 'project')
router.register(r'team', viewsets.TeamMemberViewSet)
router.register(r'story', viewsets.StoriesViewSet, 'story')
router.register(r'task', viewsets.TaskViewSet, 'task')
router.register(r'orginvite', viewsets.OrgInvitesViewset)
router.register(
	r'project-invites',
	viewsets.ProjectInviteViewSet,
	'project-invites'
)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^org_registration', views.register_member_to_org)
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
