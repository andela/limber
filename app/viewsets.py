from rest_framework.response import Response
from rest_framework import viewsets, renderers, status, permissions

from django.db import IntegrityError
from django.db.models import Q
from app.serializers import (
	OrgSerializer, UserSerializer, ProjectSerializer,
	TeamMemberSerializer, StorySerializer, MemberSerializer,
	TaskSerializer, ProjectInviteSerializer
)
from app.models.user import User, Member
from app.models.story import Story, Task
from app.models.project import Project, TeamMember
from app.models.invite import ProjectInvite


class OrgSignUpViewSet(viewsets.ModelViewSet):
	"""This is to be used to signup an organisation."""

	queryset = User.objects.filter(user_type=2)
	serializer_class = OrgSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def create(self, request):
		"""Define customizations during org creation."""
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			current_user_id = request.user.id
			# create an organisation when you call this viewset
			try:
				User.create_orgprofile(
					current_user_id, **serializer.validated_data)
				return Response(
					serializer.validated_data, status=status.HTTP_201_CREATED)
			except IntegrityError:
				return Response({
					'status': "Organisation not created",
					'message': "Organisation already exists"
				}, status=status.HTTP_400_BAD_REQUEST)
		return Response({
			'status': "Bad request",
			'message': "Failed to create an organisation"
		}, status=status.HTTP_400_BAD_REQUEST)


class UserSignUpViewSet(viewsets.ModelViewSet):
	"""This is to be used to signup a user."""

	queryset = User.objects.filter(user_type=1)
	serializer_class = UserSerializer

	def create(self, request):
		"""Define customizations during user creation."""
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			try:
				User.create_userprofile(**serializer.validated_data)
				return Response({
					'status': 'User Created',
					'message': 'User Created'
				}, status=status.HTTP_201_CREATED)
			except IntegrityError:
				return Response({
					'status': "User not created",
					'message': "User already exists"
				}, status=status.HTTP_400_BAD_REQUEST)

		return Response({
			'status': "Bad request",
			'message': "Failed to create user"
		}, status=status.HTTP_400_BAD_REQUEST)


class TeamMemberViewSet(viewsets.ModelViewSet):
	"""API endpoint that allows project team members to be viewed or edited."""

	queryset = TeamMember.objects.all()
	serializer_class = TeamMemberSerializer


class ProjectViewSet(viewsets.ModelViewSet):
	"""API endpoint that allows projects to be viewed or edited."""

	serializer_class = ProjectSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		orgs = Member.objects.filter(
			user_id=user.id).values_list('org_id', flat=True)
		users = User.objects.filter(
			Q(id=user.profile_id) | Q(id__in=orgs)).all()
		return Project.objects.filter(owner=users)

	def post_queryset(self):
		user = self.request.user
		orgs = Member.objects.filter(
			user_id=user.id).values_list('org_id', flat=True)
		users = User.objects.filter(
			Q(id=user.id) | Q(id__in=orgs)).all()
		return Project.objects.filter(owner=users)

	def create(self, request):
		"""Define customizations during user creation."""
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			Project.create_project(**serializer.validated_data)
			return Response({
				'status': 'Project Created',
				'message': 'Project Created'
			}, status=status.HTTP_201_CREATED)

		return Response({
			'status': "Bad request",
			'message': "Failed to create project"
		}, status=status.HTTP_400_BAD_REQUEST)


class StoriesViewSet(viewsets.ModelViewSet):
	"""Viewset for project stories."""

	queryset = Story.objects.all()
	serializer_class = StorySerializer
	permission_classes = (permissions.IsAuthenticated,)


class MemberViewSet(viewsets.ModelViewSet):
	queryset = Member.objects.filter()
	serializer_class = MemberSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def destroy(self, request, *args, **kwargs):
		"""This function is called when the delete http method
			is called on this viewset.

		It then calls the "remove_org_member" function in User model to remove
		members from an Organisation. The "remove_org_member" function ensures
		that organisations have an admin present at all times. It also checks
		for sufficient user privileges/ rights to perform this action.
		"""
		# id of the "remover" (current user)
		admin_id = request.user.id
		# the organisation from which a member is being removed
		org = self.get_object().org
		# the member who's being removed from the org
		member = self.get_object().user

		try:
			User.remove_org_member(admin_id=admin_id, org=org, member=member)
			return Response({
				'status': "Member successfully removed",
				'message': "Organisation member successfully removed"
			}, status=status.HTTP_200_OK)
		except Exception:
			return Response({
				'status': "Member not removed",
				'message': "Organisation member not removed"
			}, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	permission_classes = (permissions.IsAuthenticated,)


class ProjectInviteViewSet(viewsets.ModelViewSet):
	queryset = ProjectInvite.objects.all()
	serializer_class = ProjectInviteSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def create(self, request):
		"""Create ProjectInvite instance, send the email then save."""
		try:
			serializer = self.serializer_class(data=request.data)
			if serializer.is_valid():
				# create project invite instance
				project_invite = ProjectInvite(
					email=serializer.validated_data.get('email'),
					project=serializer.validated_data.get('project'),
					uid=request.user
				)

				project_invite.send_invite_email()
				project_invite.save()

				return Response(
					{
						'status': 'email sent',
						'message': 'An invitation email has been sent'
					}, status=status.HTTP_200_OK
				)
			return Response(
				{
					'status': 'Bad request',
					'message': 'Invalid data'
				}, status=status.HTTP_400_BAD_REQUEST
			)
		except Exception as e:
			return Response(
				{
					'status': 'Bad request',
					'message': 'Failed to create email invitation'
				}, status=status.HTTP_400_BAD_REQUEST
			)
