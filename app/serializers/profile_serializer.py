from rest_framework import serializers, viewsets, renderers, status, permissions
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
from app.models import User, UserAuthentication


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
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status' : "Bad request",
            'message' : "Failed to create an organisation"
        },status=status.HTTP_400_BAD_REQUEST)



# A serializer_class for signing up an organisation
class OrgSerializer(serializers.ModelSerializer):
    """This serializer class is to be used to register an organisation"""
    user_type = serializers.IntegerField(default=2, read_only=True)
    class Meta:
        model = User
        fields = ('username', 'user_type', 'name', )
        read_only_fields = ('user_type')

    # Add a create method
    def create(self, validated_data):
        return User.create_orgprofile(**validated_data)

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
