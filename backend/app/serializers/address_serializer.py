from app.models import Address
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class AddressSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model=Address
        fields=[
            'id',
            'user',
            'line1',
            'line2',
            'country',
            'city',
            'postcode',
            'updated_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
