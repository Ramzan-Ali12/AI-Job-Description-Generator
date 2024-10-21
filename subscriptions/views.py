import stripe
from django.conf import settings
from rest_framework.views import APIView
from  rest_framework import generics
from rest_framework.response import Response
from django.urls import reverse
from django.http import HttpResponse
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from subscriptions.models import Price,Subscription
from subscriptions.serializers import CheckoutSessionSerializer, CheckoutSessionResponseSerializer, PriceSerializer,CancelSubscriptionSerializer,SubscriptionSuccessSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@extend_schema(
    summary="Create new Checkout Session",
    description="Endpoint to create new checkout session for a specific plan.",
    request=CheckoutSessionSerializer,  # Attach the request schema
    responses={200: CheckoutSessionResponseSerializer},  # Attach the response schema
    tags=["subscriptions"],
    
)
class CreateCheckoutSessionView(APIView):
    serializer_class = CheckoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSessionSerializer(data=request.data)
        
        if serializer.is_valid():
            plan_uuid = serializer.validated_data['plan_uuid']
            user = request.user

            try:
                # Retrieve the price object using the provided plan_uuid
                price = Price.objects.get(uuid=plan_uuid)

                # Create a Stripe customer if not already present
                if not user.stripe_customer_id:
                    customer = stripe.Customer.create(
                        email=user.email,
                        name=user.username
                    )
                    user.stripe_customer_id = customer['id']
                    user.save()

                # Create a Stripe Checkout Session
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price': price.s_id,  # Use the Stripe price ID stored in your model
                        'quantity': 1,
                    }],
                    customer=user.stripe_customer_id,  # Attach the session to the Stripe customer
                    mode='subscription',  # For creating subscriptions
                    success_url=request.build_absolute_uri(reverse('subscription_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri('/cancel/'),
                )
                
                # Return the session URL as a response
                response_serializer = CheckoutSessionResponseSerializer({
                    'session_url': checkout_session['url']
                })
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            except Price.DoesNotExist:
                return Response({'error': 'Plan with the given UUID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Cancel Current Subscription",
    description="Cancel subscription for the current user",
    tags=["subscriptions"],
    responses={200: {"status": "Subscription canceled successfully!"}},
)
class CancelSubscriptionView(APIView):
    serializer_class = CancelSubscriptionSerializer
    def post(self, request):
        try:
            # Fetch the current authenticated user
            user = request.user
            print("user----------->")
            # Assuming `subscription_id` is stored in the user model or in a related model
            if not hasattr(user, 'subscription_id') or not user.subscription_id:
                return Response({'error': 'No subscription found for the current user'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the subscription ID from the user
            subscription_id = user.subscription_id
            print("subscription_id------------>",subscription_id)
            # Cancel the subscription in Stripe
            stripe.Subscription.delete(subscription_id)

            # Optionally, update the user's subscription status in the database
            user.subscription_status = 'canceled'  # Assuming there's a field for subscription status
            user.save()

            return Response({'status': 'Subscription canceled successfully!'}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            # Handle any Stripe-specific errors
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any other errors
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="List all available products and prices with pagination",
    description="Endpoint to list all available products and their prices with pagination",
    tags=["subscriptions"],
    responses=PriceSerializer,

)
class ListProductsView(generics.ListAPIView):
    serializer_class = PriceSerializer
    queryset = Price.objects.all()
    # add the pagination feature
    pagination_class = PageNumberPagination


from django.views import View
@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            # Retrieve customer and subscription ID
            stripe_customer_id = session['customer']
            stripe_subscription_id = session['subscription']

            # Get the user related to the Stripe customer ID (you'll need to store stripe customer_id in your User model)
            user = User.objects.get(stripe_customer_id=stripe_customer_id)  # Assuming you've stored Stripe customer ID in User model

            # Create or update the Subscription object
            subscription, created = Subscription.objects.update_or_create(
                user=user,
                defaults={
                    's_id': stripe_subscription_id,
                    'status': 'active'  # Update the status based on event type
                }
            )

        return HttpResponse(status=200)