from app.models import Address, Transaction
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class TransactionSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    address = PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'address',
            'idempotency_key',
            'amount',
            'additional_info',
            'updated_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
