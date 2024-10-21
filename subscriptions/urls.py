from django.urls import path
from subscriptions.views import CreateCheckoutSessionView, CancelSubscriptionView, ListProductsView,StripeWebhookView

urlpatterns = [
    path('subscriptions/checkout/session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('subscriptions/cancel/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
    path('subscriptions/products/', ListProductsView.as_view(), name='list_products'),
    path('subscriptions/success/', StripeWebhookView.as_view(), name='subscription_success'),
]
