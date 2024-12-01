from django.db import models
from django.contrib.auth.models import User
from main.models import Product
from django.db.models.signals import post_save

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=255, blank=True, null=True)
    shipping_country = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return "Shipping Address - " + str(self.id)
    
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping, sender=User)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=15000)
    amout_paid = models.DecimalField(decimal_places=2, max_digits=7)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order - ' + str(self.id)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return 'Order - ' + str(self.id)
