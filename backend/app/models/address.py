from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from .transaction import Transaction

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True, blank=True)

    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    country=models.CharField(max_length=63)
    city=models.CharField(max_length=127)
    postcode=models.CharField(max_length=15)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.line1}, {self.line2}'
