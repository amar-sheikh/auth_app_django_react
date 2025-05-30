from app.models import Address, Transaction
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class AddressSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    transaction = PrimaryKeyRelatedField(
        queryset=Transaction.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model=Address
        fields=[
            'id',
            'user',
            'transaction',
            'line1',
            'line2',
            'country',
            'city',
            'postcode',
            'updated_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
