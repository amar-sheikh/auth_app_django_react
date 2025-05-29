from app.models import Transaction
from app.serializers import TransactionSerializer
from rest_framework.viewsets import ModelViewSet

class TransactionViewSet(ModelViewSet):
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer
