from app.models import Transaction, Address
from app.serializers import TransactionSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class TransactionViewSet(ModelViewSet):
    serializer_class=TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def without_address(self, request):
        queryset = self.get_queryset().filter(address=None)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        current_address = request.user.current_address

        if current_address:
            current_address.transaction = instance
            current_address.save(update_fields=['transaction'])

            request.user.current_address = None
            request.user.save(update_fields=['current_address'])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
