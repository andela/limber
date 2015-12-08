from rest_framework import serializers
from app.models.user import User
from app.models.project import Project, TeamMember


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


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    # team_members = serializers.HyperlinkedRelatedField(queryset=TeamMember.objects.all(), view_name='teammember-detail', many=True)
    team_members = serializers.SlugRelatedField(many=True, read_only=True, slug_field='user_id')

    class Meta:
        model = Project
        fields = ('url', 'owner', 'project_name', 'project_desc', 'team_members')

    def get_owner(self, obj):
        return obj.owner.id



class TeamMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type=1),
     )

    user_level = serializers.ChoiceField([1, 2])
    class Meta:
        model = TeamMember
        fields = ('url', 'user', 'project', 'user_level')

