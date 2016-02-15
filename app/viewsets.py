from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from django.db import IntegrityError
from django.db.models import Q
from app.serializers import (

	OrgSerializer, UserSerializer, ProjectSerializer,
	TeamMemberSerializer, StorySerializer, MemberSerializer,
	TaskSerializer, ProjectInviteSerializer, OrgInviteSerilizer

)
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser
from app.models.user import User, Member, UserAuthentication
from app.models.story import Story, Task
from app.models.project import Project, TeamMember
from app.models.invite import ProjectInvite
from app.models.org_invite import OrgInvites


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

	def create(self, request):
		"""Define customizations during addition of members to a project."""

		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			team_member = TeamMember(**serializer.validated_data)
			team_member.save()
			return Response(
				{
					'status': 'Created',
					'message': 'Team Member Created'
				},
				status=status.HTTP_201_CREATED
			)
		return Response(
			{
				'status': 'Invalid data',
				'message': 'Invalid data provided'
			}, status=status.HTTP_400_BAD_REQUEST
		)


class PersonalProjectViewSet(viewsets.ReadOnlyModelViewSet):
	"""API endpoint to view current user's personal projects."""

	serializer_class = ProjectSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		current_user = self.request.user
		user = User.objects.filter(id=current_user.profile_id).all()
		return Project.objects.filter(owner=user)


class OrgProjectViewSet(viewsets.ReadOnlyModelViewSet):

	"""API endpoint to view projects for organisations the user belongs in."""

	serializer_class = ProjectSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		current_user = self.request.user
		user_orgs = Member.objects.filter(
			user_id=current_user.id).values_list('org_id', flat=True)
		user_in_team = TeamMember.objects.filter(
			user_id=current_user.id).values_list('project_id', flat=True)
		orgs = User.objects.filter(id__in=user_orgs).all()
		return Project.objects.filter(project_id__in=user_in_team, owner=orgs)


class OtherProjectViewSet(viewsets.ReadOnlyModelViewSet):

	"""API endpoint to view projects by othe users, in which the
	current user is a team member.
"""

	serializer_class = ProjectSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		current_user = self.request.user
		user_orgs = Member.objects.filter(
			user_id=current_user.id).values_list('org_id', flat=True)
		user_in_team = TeamMember.objects.filter(
			user_id=current_user.id).values_list('project_id', flat=True)
		orgs = User.objects.filter(
			Q(id=current_user.profile_id) | Q(id__in=user_orgs)).all()

		return Project.objects.filter(project_id__in=user_in_team).exclude(owner=orgs)


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
		"""Define customizations during project creation."""
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
	""" Viewset for project stories """

	queryset = Story.objects.all()
	serializer_class = StorySerializer
	permission_classes = (permissions.IsAuthenticated,)


class OrgInvitesViewset(viewsets.ModelViewSet):
	""" Handles Invitation of Members to Organisation"""
	queryset = OrgInvites.objects.all()
	serializer_class = OrgInviteSerilizer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def list(self, request):
		queryset = OrgInvites.objects.all()
		serializer = OrgInviteSerilizer(queryset, many=True)
		return Response(serializer.data)

	def get_queryset(self):
		# Override the GET method query to only show logged in user
		obj = OrgInvites.objects.filter(
			Q(uid=self.request.user.id)).first()
		return obj

	def retrieve(self, request, pk=None):
		# retrieve and   and registers a user
		orginvitation = OrgInvites.objects.get(code=pk)
		email = orginvitation.email
		if not email:
			return Response({
				'Error': 'Invalid Code',
			}, status=status.HTTP_400_BAD_REQUEST)
		if 'register' in request.query_params:
			# check if email belongs to a registered user

			try:
				user = UserAuthentication.objects.get(email=email)
				if hasattr(request.user, 'email'):
					if user.email == request.user.email:
						org = orginvitation.org_id
						org = User.objects.get(id=org)
						# Add member to Members Org
						member = Member.objects.create(
							org=org, user=user, user_level=2)
						# Change flag in OrgInvitation Table to 2
						orginvitation.accept = 1
						orginvitation.save()
						return Response({
							'org': org.id,
							'user': user.id,
							'member': member.id
						}, status.HTTP_201_CREATED)
				# check if he is current logged in user
				return Response({
					'Message': 'Please Login',
					'email': email
				}, status.HTTP_403_FORBIDDEN)

			except UserAuthentication.DoesNotExist:
				# Else send user to sign
				return Response({
					'message': 'please Signup then try again',
					'email': email
				}, status.HTTP_428_PRECONDITION_REQUIRED)
		# return detail about the invitation
		serializer = self.serializer_class(orginvitation)
		return Response(serializer.data, status.HTTP_200_OK)

	def create(self, request):
		# restrict ID of creator to the
		request.data['uid'] = request.user.id
		serializer = self.serializer_class(data=request.data)
		# Check if emain belongs to an existing user
		userid = UserAuthentication.objects.filter(email=request.data['email'])
		user = Member.objects.filter(user=userid, org=request.data['org'])
		if user:
			return Response({
							'error': 'Member already belongs to Organisation',
							}, status.HTTP_400_BAD_REQUEST)
		if serializer.is_valid():
			invite = OrgInvites.objects.create(**serializer.validated_data)
			if invite is not None:
				return Response({
					'status': "email Created",
					'code': invite.code,
				}, status=status.HTTP_201_CREATED)
			return Response({
				'message': 'Mail notification was not sent',

			}, status=status.HTTP_400_BAD_REQUEST)
		return Response(
			serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

	def create(self, request):
		"""Create ProjectInvite instance, send the email then save."""
		if isinstance(request.user, AnonymousUser):
			return Response(
				{
					'detail': 'Authentication credentials were not provided.'
				}, status=status.HTTP_401_UNAUTHORIZED
			)
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

	def retrieve(self, request, pk=None):
		"""Retrieve ProjectInvite object from database when its id is specified.

		Check if email in invite object belongs to a user in the system. If it does,
		add that user as a project member of the project in the invite object.

		If the email in the invite has no associated user in the system, return a
		response indicating that the invited user doesn't exist in the system.
		"""
		# Handle the edge case where the ProjectInvite doesn't exist in the DB
		# (Return a 404 response code if it doesn't exist)
		try:
			project_invite = ProjectInvite.objects.get(pk=pk)
		except ProjectInvite.DoesNotExist:
			return Response(
				{
					'detail': 'Not found.'
				}, status=status.HTTP_404_NOT_FOUND
			)
		# check if email in invite belongs to user who already exists
		try:
			user_auth = UserAuthentication.objects.get(email=project_invite.email)
			# user already exists in system

			return Response(
				{
					'status': 'User found',
					'message': 'User exists in the system'
				}, status=status.HTTP_200_OK
			)
		except UserAuthentication.DoesNotExist:
			# user doesn't exist
			return Response(
				{
					'status': 'User not found',
					'message': 'User does not exist in the system'
				}, status=status.HTTP_404_NOT_FOUND
			)

	def update(self, request, pk=None):
		"""Encapsulate logic that executes when a HTTP PUT method is sent.

		(To be used only when a project invite has been ACCEPTED).
		"""
		# ALGORITHM
		# 1. retrieve the project invite object from the database
		# 2. Check that the email from the request matches the email in the invite
		# 3. Get the user object by filtering the query by the email in the invite
		# (this means users MUST exist in the system beforehand)
		# 4. With the user and project info, invitee is added as project member
		# 5. Update project invite to status accepted
		if isinstance(request.user, AnonymousUser):
			return Response(
				{
					'detail': 'Authentication credentials were not provided.'
				}, status=status.HTTP_401_UNAUTHORIZED
			)

		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			try:
				pi = ProjectInvite.objects.get(pk=self.kwargs.get('pk', None))

				if serializer.data.get('email') != pi.email:
					return Response(
						{
							'status': 'Invite not processed',
							'message': 'Login email does not match invited email!'
						}, status=status.HTTP_400_BAD_REQUEST
					)
				try:
					user_auth = UserAuthentication.objects.get(email=pi.email)

					tm = TeamMember(user=user_auth, project=pi.project, user_level=0)
					tm.save()
					pi.accept = ProjectInvite.ACCEPTED
					pi.save()
					return Response(
						{
							'status': 'Project invite accepted',
							'message': 'Project invite accepted'
						}, status=status.HTTP_200_OK
					)
				except UserAuthentication.DoesNotExist:
					return Response(
						{
							'detail': 'User not found.'
						}, status=status.HTTP_404_NOT_FOUND
					)
			except ProjectInvite.DoesNotExist:
				return Response(
					{
						'detail': 'Project invite not found.'
					}, status=status.HTTP_404_NOT_FOUND
				)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def destroy(self, request, pk=None):
		if isinstance(request.user, AnonymousUser):
			return Response(
				{
					'detail': 'Authentication credentials were not provided.'
				}, status=status.HTTP_401_UNAUTHORIZED
			)

		try:
			pi = ProjectInvite.objects.get(pk=pk)
			pi.delete()
			return Response({}, status=status.HTTP_204_NO_CONTENT)
		except ProjectInvite.DoesNotExist:
			return Response(
				{
					'detail': 'Not found.'
				}, status=status.HTTP_404_NOT_FOUND
			)
