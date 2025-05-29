from app.models import Profile, Address
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class ProfileSerializer(ModelSerializer):
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all())
    current_address_id = PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_id',
            'current_address_id'
            'updated_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
