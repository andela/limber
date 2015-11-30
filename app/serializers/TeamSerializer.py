from rest_framework import serializers, viewsets
from rest_framework.decorators import detail_route
from rest_framework import renderers
from app.models import Project, Team, User, UserProfile
import ipdb


class TeamSerializer(serializers.ModelSerializer):
	user_id = serializers.PrimaryKeyRelatedField(
		label="User",
        queryset=UserProfile.objects.all(),
     )
	project_id = serializers.PrimaryKeyRelatedField(
		label="Project",
        queryset=Project.objects.select_related(),
     )
	user_level = serializers.ChoiceField([1, 2])
	class Meta:
		model = Team
		fields = ('url', 'user_id', 'project_id', 'user_level')


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

