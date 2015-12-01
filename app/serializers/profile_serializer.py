from rest_framework import serializers, viewsets, renderers, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from app.models import Account, Profile

class AccountSerializer(serializers.ModelSerializer):
    """docstring for AccountSerializer"""
    # profile_id = ProfileSerializer()
    class Meta:
        model = Account
        fields = ('email','first_name','last_name','is_admin',)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class ProfileSerializer(serializers.ModelSerializer):
    """docstring for ProfileSerializer"""
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=False
    )


    class Meta:
        """docstring for Meta"""
        model = Profile
        fields = ('username', 'user_type', 'email', 'password',)
        write_only_fields = ('email', 'password',)

    # Add a create method
    def create(self, validated_data):
        if validated_data.get('user_type') == 2:
            return Profile.create_orgprofile(**validated_data)
        elif validated_data.get('user_type') == 1:
            return Profile.create_userprofile(**validated_data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #
    # @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_type = int(request.data.get('user_type'))
            if user_type == 1:
                import ipdb; ipdb.set_trace()

                Profile.create_userprofile(**serializer.validated_data)
            elif user_type == 2:
                Profile.create_orgprofile(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status' : 'Bad request',
            'message' : 'Failed to create user'
        },status=status.HTTP_400_BAD_REQUEST)
