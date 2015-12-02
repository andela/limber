from rest_framework import serializers, viewsets, renderers, status
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
from app.models import User, UserAuthentication

class UserAuthenticationSerializer(serializers.ModelSerializer):
    """This serializer class maps the UserAuthentication Model"""
    class Meta:
        model = UserAuthentication
        fields = ('email','password',)

    def create(self, validated_data):
        pass


class LoginViewSet(viewsets.ModelViewSet):
    """This viewset class handles UserAuthenticationSerializer"""
    queryset = UserAuthentication.objects.all()
    serializer_class = UserAuthenticationSerializer
    
    def create(self, request):
        pass


# A serializer_class for signing up a user
class UserSerializer(serializers.ModelSerializer):
    """This serializer class is to be used to register a user"""
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=False
    )

    class Meta:
        model = User
        fields = ('username', 'user_type', 'email', 'password',)
        write_only_fields = ('email', 'password',)

    # Add a create method
    def create(self, validated_data):
        return User.create_userprofile(**validated_data)

# A serializer_view_set class for creating a user
class UserSignUpViewSet(viewsets.ModelViewSet):
    """This is to be used to signup a user"""
    queryset = User.objects.all()
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
    # user_type = serializers.
    class Meta:
        model = User
        fields = ('username', 'user_type', 'name', )

    # Add a create method
    def create(self, validated_data):
        return User.create_orgprofile(**validated_data)

# A serializer_view_set class for creating an organisation
class OrgSignUpViewSet(viewsets.ModelViewSet):
    """This is to be used to signup an organisation"""
    queryset = User.objects.all()
    serializer_class = OrgSerializer

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
