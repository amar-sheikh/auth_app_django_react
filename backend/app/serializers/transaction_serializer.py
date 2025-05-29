from app.models import Transaction
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class TransactionSerializer(ModelSerializer):
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all())

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
