from app.models import Address, Transaction
from app.serializers import AddressSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

class AddressViewSet(ModelViewSet):
    serializer_class=AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current_address(self, request):
        if request.user.current_address and not request.user.current_address.transactions.exists():
            return Response({ 'current_address': self.get_serializer(request.user.current_address).data })
        return Response({ 'current_address': None })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        Transaction.objects.filter(address=None).update(address=instance)

        if not instance.transactions.exists() and (not request.user.current_address or request.user.current_address.transactions.exists()):
            request.user.current_address = instance
            request.user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
