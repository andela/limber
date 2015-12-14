from rest_framework.response import Response
from rest_framework import viewsets, renderers, status, permissions

from app.serializers import OrgSerializer, UserSerializer
from app.models.user import User

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
