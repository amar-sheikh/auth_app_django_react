from app.models import Address
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    current_address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    email = models.EmailField(_("email address"), blank=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.email:
            return f'{self.username} - {self.email}'
        else:
            return self.username
