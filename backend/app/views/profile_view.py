from app.models import Profile
from app.serializers import ProfileSerializer
from rest_framework.viewsets import ModelViewSet

class ProfileViewSet(ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
