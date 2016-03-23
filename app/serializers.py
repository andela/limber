from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from itertools import chain
from django.db.models import Q
from app.models.story import Story, Task
from app.models.user import User, Member, UserAuthentication
from app.models.project import Project, TeamMember
from app.models.org_invite import OrgInvites
from app.models.invite import ProjectInvite
from app.models.pass_reset import PasswordReset


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
    org_id = serializers.CharField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'user_type', 'full_name', 'org_id')
        read_only_fields = ('user_type')

    def create(self, validated_data):
        """Modify default method to create organisation."""
        return User.create_orgprofile(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):

    """Serializer class to be used for projects."""

    team_members = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='user_id')
    project_id = serializers.IntegerField(read_only=True)

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
        fields = (
            'url', 'owner', 'project_name', 'project_desc', 'team_members',
            'project_id',
        )

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
        fields = ('email', 'code', 'org', 'accept', 'uid')
        validators = [
            UniqueTogetherValidator(
                queryset=OrgInvites.objects.filter(accept=0),
                fields=('email', 'org'),
                message='Invitation  Already exist'
            )
        ]


# A serializer to add members to an existing org
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('url', 'org', 'user', 'user_level')
        validators = [
            UniqueTogetherValidator(
                queryset=Member.objects.filter(),
                fields=('user', 'org'),
                message='User is already a member'
            )
        ]

    def get_fields(self, *args, **kwargs):
        fields = super(MemberSerializer, self).get_fields(*args, **kwargs)
        if self.context:
            fields['org'].queryset = fields['org'].queryset.filter(
                user_type=2
            ).all()
        return fields


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class ProjectInviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectInvite
        fields = ('email', 'project', 'accept')


class PasswordResetSerializer(serializers.ModelSerializer):
    """Serializer to represent data from PasswordReset model in JSON format."""

    class Meta:
        model = PasswordReset
        fields = ('user', 'request_date',)
        # write_only_fields = ('email', 'password',)
        read_only_fields = ('reset_code')