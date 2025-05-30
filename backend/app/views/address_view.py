from app.models import Address
from app.serializers import AddressSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class AddressViewSet(ModelViewSet):
    serializer_class=AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def non_transaction_count(self, request):
        return Response({ 'count': self.get_queryset().filter(transaction=None).count() })
