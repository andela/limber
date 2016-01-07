from rest_framework import serializers
from itertools import chain
from django.db.models import Q
from app.models.story import Story
from app.models.user import User, Member
from app.models.project import Project, TeamMember
from app.models.pending import OrgInvites
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
	"""This serializer class is to be used to register a user."""

	email = serializers.EmailField(write_only=True, required=False)
	password = serializers.CharField(
		style={'input_type': 'password'}, write_only=True, required=False
	)
	user_type = serializers.IntegerField(default=1, read_only=True)

	class Meta:
		model = User
		fields = ('username', 'user_type', 'email', 'password',)
		write_only_fields = ('email', 'password',)
		read_only_fields = ('user_type')

	def create(self, validated_data):
		"""Modify default method to create user."""
		return User.create_userprofile(**validated_data)


class OrgSerializer(serializers.ModelSerializer):
	"""This serializer class is to be used to register an organisation."""

	user_type = serializers.IntegerField(default=2, read_only=True)

	class Meta:
		model = User
		fields = ('username', 'user_type', 'full_name')
		read_only_fields = ('user_type')

	def create(self, validated_data):
		"""Modify default method to create organisation."""
		return User.create_orgprofile(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):
	"""Serializer class to be used for projects."""

	team_members = serializers.SlugRelatedField(
		many=True, read_only=True, slug_field='user_id')

	def get_fields(self, *args, **kwargs):
		"""Method to filter the choices presented for project owner."""
		fields = super(ProjectSerializer, self).get_fields(*args, **kwargs)
		if self.context:
			user = self.context['request'].user
			view = self.context['view']
			orgs = Member.objects.filter(
				user_id=user.id).values_list('org_id', flat=True)
			fields['owner'].queryset = fields['owner'].queryset.filter(
				Q(id=user.profile_id) | Q(id__in=orgs)).all()
		return fields

	class Meta:
		model = Project
		fields = ('url', 'owner', 'project_name', 'project_desc', 'team_members')
		validators = [
			UniqueTogetherValidator(
				queryset=Project.objects.all(),
				fields=('owner', 'project_name'),
				message='User already has a project by that name'
			)
		]

	def create(self, validated_data):
		"""Customize default method to create project."""
		return Project.create_project(**validated_data)


class TeamMemberSerializer(serializers.ModelSerializer):
	"""Serializer class to be used for project members."""

	user = serializers.PrimaryKeyRelatedField(
		queryset=User.objects.filter(user_type=1),
	)
	user_level = serializers.ChoiceField([1, 2])

	class Meta:
		model = TeamMember
		fields = ('url', 'user', 'project', 'user_level')
		validators = [
			UniqueTogetherValidator(
				queryset=TeamMember.objects.all(),
				fields=('user', 'project'),
				message='User exists in the list of team members for this project'
			)
		]


class StorySerializer(serializers.ModelSerializer):
	"""Serializer class for project stories"""

	class Meta:
		model = Story
		fields = '__all__'

class OrgInviteSerilizer (serializers.ModelSerializer):
	''' Serializer for Invitation of Members to Organisations '''
	code = serializers.CharField(required=False, read_only=True)

	class Meta:
	    model = OrgInvites
	    fields = ('url','code','email', 'org', 'uid', 'accept')