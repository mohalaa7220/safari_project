from django.db import models
from users.models import User
from products.models import Product


class Report(models.Model):
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='user_reports', null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name='product_reports', null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created',)
