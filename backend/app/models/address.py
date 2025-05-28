from django.contrib.auth.models import User
from django.db import models

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    country=models.CharField(max_length=63)
    city=models.CharField(max_length=127)
    postcode=models.CharField(max_length=15)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.line1}, {self.line2}'
