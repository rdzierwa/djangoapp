from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission

class Company(models.Model):
    name = models.CharField(max_length=255)
    # inne pola charakteryzujące firmę

class Warehouse(models.Model):
    users = models.ManyToManyField(User, related_name='warehouses')
    name = models.CharField(max_length=100, unique=True)

    url = models.TextField()
    credentials = models.TextField()
    
class Product(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    ean = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    warehouses = models.ManyToManyField(Warehouse)

    class Meta:
        ordering = ['sku']

class ProductQty(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    update_date = models.DateField(auto_now=True)
    wh_product_id = models.CharField(max_length=50)

    class Meta:
        unique_together = ['warehouse', 'product']

class Synchronization(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    last_synch = models.DateField(auto_now=True)
    sum_qty = models.BooleanField(default=False)
    synch = models.BooleanField(default=False)

    class Meta:
        ordering = ['last_synch']
