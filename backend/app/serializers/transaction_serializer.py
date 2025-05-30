from app.models import Transaction
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class TransactionSerializer(ModelSerializer):
    user_id = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user_id',
            'idempotency_key',
            'amount',
            'additional_info',
            'updated_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
