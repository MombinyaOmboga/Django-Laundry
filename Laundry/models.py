from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    clothes_amount = models.PositiveIntegerField(default=1)
    is_verified = models.Boolean(default=False)
    total_amount = models.PositiveIntegerField(null=True, blank=True)

class ServiceCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Checkout(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=233)
    email_id = models.EmailField(max_length=255)
    delivery_address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
