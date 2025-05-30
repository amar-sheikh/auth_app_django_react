from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid1

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')

    idempotency_key = models.UUIDField(default=uuid1, editable=False, unique=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.idempotency_key)
