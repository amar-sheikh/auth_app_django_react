from app.models import Address
from app.serializers import AddressSerializer
from rest_framework.viewsets import ModelViewSet

class AddressViewSet(ModelViewSet):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer
