from rest_framework import serializers
from .models import Price

# Serializer for the Checkout Session input and output
class CheckoutSessionSerializer(serializers.Serializer):
    plan_uuid = serializers.UUIDField(required=True) 

# Serializer for the response after creating the checkout session
class CheckoutSessionResponseSerializer(serializers.Serializer):
    session_url = serializers.URLField() 


# Serializer for the Price model
class PriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)  # Include product name

    class Meta:
        model = Price
        fields = ['uuid', 's_id', 'currency', 'nickname', 'recurring_interval', 'recurring_interval_count', 'price', 'product_name']

# Serializer to validate subscription cancellation request
class CancelSubscriptionSerializer(serializers.Serializer):
    #subscription_id = serializers.CharField(required=True)
    pass

class SubscriptionSuccessSerializer(serializers.Serializer):
    pass