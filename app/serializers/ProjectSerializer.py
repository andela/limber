from rest_framework import serializers, viewsets
from rest_framework.decorators import detail_route
from rest_framework import renderers
from app.models import Project, UserProfile
import ipdb

class ProjectSerializer(serializers.ModelSerializer):
	owner_id = serializers.SerializerMethodField()
	class Meta:
		model = Project
		fields = ('url', 'owner_id', 'project_name', 'project_desc')

	def get_owner_id(self, obj):
		return obj.owner_id.user.id

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        current_user = UserProfile.objects.get(user_id=self.request.user.id)
        serializer.save(owner_id=current_user)