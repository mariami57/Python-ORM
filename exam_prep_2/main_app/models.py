from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.managers import ProfileManager
from main_app.mixins import CreteDateMixin

# Create your models here.

class Profile(CreteDateMixin):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    objects = ProfileManager()


class Product(CreteDateMixin):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)])
    in_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)

class Order(CreteDateMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='customer_orders')
    products = models.ManyToManyField(Product)
    total_price=models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.1)])
    is_completed = models.BooleanField(default=False)
