from rest_framework.response import Response
from rest_framework import viewsets, renderers, status, permissions

from serializers import OrgSerializer, UserSerializer, ProjectSerializer, TeamSerializer
from app.models.user import User
from app.models.project import Project, Team
from rest_framework.decorators import detail_route


# A serializer_view_set class for creating an organisation
class OrgSignUpViewSet(viewsets.ModelViewSet):
    """This is to be used to signup an organisation"""
    queryset = User.objects.filter(user_type=2)
    serializer_class = OrgSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # create an organisation when you call this viewset
            User.create_orgprofile(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status' : "Bad request",
            'message' : "Failed to create an organisation"
        },status=status.HTTP_400_BAD_REQUEST)

# A serializer_view_set class for creating a user
class UserSignUpViewSet(viewsets.ModelViewSet):
    """This is to be used to signup a user"""
    queryset = User.objects.filter(user_type=1)
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # create a user when you call this viewset
            User.create_userprofile(**serializer.validated_data)
            return Response({
                    'status': 'User Created',
                    'message': 'User Created'
                },
                status=status.HTTP_201_CREATED)

        return Response({
            'status' : "Bad request",
            'message' : "Failed to create user"
        },status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        current_user = User.objects.get(id=self.request.user.id)
        serializer.save(owner_id=current_user)