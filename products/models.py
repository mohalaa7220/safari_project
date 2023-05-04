from django.db import models
from users.models import Employee
from django.urls import reverse


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='employee_product')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    image = models.ImageField(
        upload_to='product_images', blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.name

    @property
    def qr_code_url(self):
        return (reverse('qr_code', args=[self.pk]))

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.in_stock = False
        else:
            self.in_stock = True
        super().save(*args, **kwargs)
