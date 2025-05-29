from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    idempotency_key = models.UUIDField(unique=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.idempotency_key)
