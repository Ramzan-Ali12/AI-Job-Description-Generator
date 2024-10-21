import uuid
import stripe
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
stripe.api_key = settings.STRIPE_SECRET_KEY
#print("Stripe API Key-------------->",stripe.api_key)


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    s_id = models.CharField(max_length=100)


    def save(self, **kwargs):
        if not self.s_id:
             # Create a product in Stripe and get the product ID
            stripe_product = stripe.Product.create(name=self.name)
            self.s_id = stripe_product['id']
        super().save(**kwargs)

    def __str__(self):
        return self.name


class Price(models.Model):
    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(Product, related_name='prices', on_delete=models.CASCADE)
    s_id = models.CharField(max_length=100)
    currency = models.CharField(max_length=3, default='USD')
    nickname = models.CharField(max_length=100, blank=True)
    recurring_interval = models.CharField(max_length=10, default='month')
    recurring_interval_count = models.IntegerField(default=1)
    price = models.IntegerField(default=0)  # stored as cents
    type = models.CharField(max_length=50, default='recurring')


    def save(self, **kwargs):
        if not self.s_id:
             # Create a price in Stripe and get the price ID
            stripe_price = stripe.Price.create(
                product=self.product.s_id,
                currency=self.currency,
                nickname=self.nickname,
                recurring={
                    'interval': self.recurring_interval,
                    'interval_count': self.recurring_interval_count
                },
                unit_amount=self.price
            )
            print("Stripe Price--------->",stripe_price)
            self.s_id = stripe_price['id']

        super().save(**kwargs)


    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
        ('unpaid', 'Unpaid'),
        ('trialing', 'Trialing'),
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    s_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')  # Using choices here



    def __str__(self):
        return self.user.username