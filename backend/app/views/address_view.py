from app.models import Address
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
        if request.user.current_address:
            return Response({ 'current_address': self.get_serializer(request.user.current_address).data })
        else:
            return Response({ 'current_address': None })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if not request.user.current_address:
            request.user.current_address = instance
            request.user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if instance.transaction is not None:
            request.user.current_address = None
            request.user.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
