from app.models import Transaction
from app.serializers import TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

class TransactionViewSet(ModelViewSet):
    serializer_class=TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def count(self, request):
        return Response({ 'count': self.get_queryset().count() })
