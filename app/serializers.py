from rest_framework import serializers
from app.models import Project, Team


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
	owner_id = serializers.ReadOnlyField(source='owner.user_id')
	class Meta:
		model = Project
		fields = ('url', 'owner_id', 'project_name', 'project_desc')

class TeamSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Team
		fields = ('url', 'user_id', 'project_id', 'user_level')