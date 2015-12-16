from rest_framework import serializers
from itertools import chain
from django.db.models import Q

from app.models.user import User, Member
from app.models.project import Project, TeamMember
from rest_framework.validators import UniqueTogetherValidator


# A serializer_class for signing up a user
class UserSerializer(serializers.ModelSerializer):
	"""This serializer class is to be used to register a user"""
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
	# Add a create method
	def create(self, validated_data):
		return User.create_userprofile(**validated_data)


# A serializer_class for signing up an organisation
class OrgSerializer(serializers.ModelSerializer):
	"""This serializer class is to be used to register an organisation"""
	user_type = serializers.IntegerField(default=2, read_only=True)
	class Meta:
		model = User
		fields = ('username', 'user_type', 'full_name' )
		read_only_fields = ('user_type')

	# Add a create method
	def create(self, validated_data):
		return User.create_orgprofile(**validated_data)


class UserlistingSerialization(serializers.RelatedField):
	def to_representation(self, value):
		return '{}'.format(value.id)

	def display_value(self, value):
		return '{}'.format(value.username)

	def to_internal_value(self, value):
		return int(value)


class ProjectSerializer(serializers.ModelSerializer):

	team_members = serializers.SlugRelatedField(many=True, read_only=True, slug_field='user_id')

	def get_fields(self, *args, **kwargs):
		fields = super(ProjectSerializer, self).get_fields(*args, **kwargs)
		if self.context:
			user = self.context['request'].user
			view = self.context['view']
			orgs = Member.objects.filter(user_id=user.id).values_list('org_id', flat=True)
			fields['owner'].queryset = fields['owner'].queryset.filter(Q(id=user.profile_id)| Q(id__in=orgs)).all()
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
		return Project.create_project(**validated_data)


class TeamMemberSerializer(serializers.ModelSerializer):
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
				message='User already exists in the list of team members for this project'
			)
		]

