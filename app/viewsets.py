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
		"""Create user and add him/her to project members table if query parameter
		exists. Simply create user if query parameter doesn't exist."""
		if request.query_params:
			try:
				invite_code = request.query_params.get('invite', None)
				if invite_code:
					# confirm validity of invite code supplied
					pi_object = get_object_or_404(ProjectInvite, pk=invite_code)
					if pi_object:
						# email in invite object should be email from request
						if pi_object.email == request.data.get('email'):
							# create the user in the system
							self.signup_user(request)
							# add the user as a member on the project
							user_auth = UserAuthentication.objects.get(
								email=pi_object.email
							)
							team = TeamMember(
								user=user_auth.profile,
								project=pi_object.project,
								user_level=2
							)
							team.save()
							# update invites table
							pi_object.accept = ProjectInvite.ACCEPTED
							pi_object.save()
							return Response(
								{
									'status': 'Invitation successful',
									'message': 'New user created and added to project'
								}, status=status.HTTP_201_CREATED
							)
						else:
							raise Exception('Attempt to sign up uninvited user!')
			except IntegrityError:
				return Response(
					{
						'status': "User not created",
						'message': "User already exists"
					}, status=status.HTTP_400_BAD_REQUEST
				)
			except Exception:
				return Response(
					{
						'status': "Bad request",
						'message': "Failed to create user"
					}, status=status.HTTP_400_BAD_REQUEST
				)

		else:
			try:
				self.signup_user(request)
				return Response(
					{
						'status': 'User Created',
						'message': 'User Created'
					}, status=status.HTTP_201_CREATED
				)
			except IntegrityError:
				return Response(
					{
						'status': "User not created",
						'message': "User already exists"
					}, status=status.HTTP_400_BAD_REQUEST
				)
			except Exception:
				return Response(
					{
						'status': "Bad request",
						'message': "Failed to create user"
					}, status=status.HTTP_400_BAD_REQUEST
				)

	def signup_user(self, request):
		"""Create new user with username, email and password."""
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			try:
				User.create_userprofile(**serializer.validated_data)
			except IntegrityError:
				raise IntegrityError('User already exists')
		else:
			raise Exception('Invalid data')


class TeamMemberViewSet(viewsets.ModelViewSet):
	"""API endpoint that allows project team members to be viewed or edited."""

	queryset = TeamMember.objects.all()
	serializer_class = TeamMemberSerializer


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

	def retrieve(self, request, pk=None):
		"""Retrieve the ProjectInvite object from the database, then direct to
		either signup or signin depending on whether the invited user exists in
		the system.

		This get request is processed when the user chooses to accept a project
		invitation.
		"""
		# Handle the edge case where the ProjectInvite doesn't exist in the DB
		# Return a 404 response if it doesn't exist
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
			user = UserAuthentication.objects.get(email=project_invite.email)
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
		"""Retrieve the ProjectInvite object from the database then update the
		accept status of this object.

		This put request is processed when the user chooses to reject a project
		invitation.
		"""
		# Handle the edge case where the ProjectInvite doesn't exist in the DB
		# Return a 404 response if it doesn't exist
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			try:
				project_invite = ProjectInvite.objects.get(pk=pk)
			except ProjectInvite.DoesNotExist:
				return Response(
					{
						'detail': 'Not found.'
					}, status=status.HTTP_404_NOT_FOUND
				)
			project_invite.accept = ProjectInvite.REJECTED
			project_invite.save()
			return Response(
				{
					'status': 'Invite updated',
					'message': 'Accept status updated'
				}
			)
		return Response(
			{
				'status': 'Bad request',
				'message': 'Invalid data'
			}, status=status.HTTP_400_BAD_REQUEST
		)
