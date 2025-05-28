from django.contrib.auth.models import User
from django.db import models
from .address import Address

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_address')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user.email:
            return f'{self.user.username} - {self.user.email}'
        else:
            return self.user.username
