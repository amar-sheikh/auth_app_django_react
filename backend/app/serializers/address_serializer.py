from app.models import Address, Transaction
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class AddressSerializer(ModelSerializer):
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all())
    transaction_id = PrimaryKeyRelatedField(queryset=Transaction.objects.all())

    class Meta:
        model=Address
        fields=[
            'id',
            'user_id',
            'transaction_id',
            'line1',
            'line2',
            'country',
            'city',
            'postcode',
            'updated_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
