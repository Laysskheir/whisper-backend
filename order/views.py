# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import stripe
from .serializers import OrderSerializer

from config import settings
from .models import Order
from rest_framework.views import APIView
from user.models import User
from django.http import HttpResponse, JsonResponse
from django.views import View

import logging

logger = logging.getLogger(__name__)


class OrderView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreOrderView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            order_data = request.data

            # # Extract additional information
            # phone = order_data.get('phone')
            # ispaid = order_data.get('ispaid', False)

            order = Order.objects.create(
                user=request.user,
                total_amount=order_data.get("totalAmount", 0),
                order_status=True,
                # phone=phone,
                # ispaid=ispaid,
            )

            product_ids = order_data.get("productIds", [])
            order.products.set(product_ids)

            return Response(
                {"message": "Order stored successfully"}, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateCheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # Extract cartItems from the request data
            cart_items = request.data.get("cartItems", [])

            # Create a list of line items for the Checkout session
            line_items = []
            for item in cart_items:
                line_items.append(
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": item["name"],
                            },
                            "unit_amount": item["price"] * 100,
                        },
                        "quantity": item["quantity"],
                    }
                )

            # Create a Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                # billing_address_collection="required",
                # phone_number_collection={"enabled": True},
                mode="payment",
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL,
            )

            # You may want to associate the session with the order here

            # Return the session ID to the frontend
            return Response({"sessionId": session["id"]})

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            logger.error(f"Error in stripe webhook while constructing event {e}")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Error in stripe webhook while constructing event {e}")
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            print("Payment successful")
             #session = event["data"]["object"]

            # customer_email = session["customer_details"]["email"]
            # order_id = session["metadata"]["order_id"]

            # payment = Order.objects.get(pk=order_id)
            # payment.status = "C"
            # payment.save()

            # send_email_async.delay(
            #     to_email=customer_email,
            #     subject="Thank you for purchasing",
            #     message=f"Your order {order_id} have been placed",
            #     from_email="shopapi89@gmail.com",
            # )

        return HttpResponse(status=200)


# class StripeWebhookView(View):
#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         payload = request.body
#         sig_header = request.headers.get("Stripe-Signature", None)

#         # Replace 'your_stripe_endpoint_secret' with your actual endpoint secret
#         endpoint_secret = "your_stripe_endpoint_secret"

#         try:
#             event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#         except ValueError as e:
#             # Invalid payload
#             return JsonResponse({"error": str(e)}, status=400)
#         except stripe.error.SignatureVerificationError as e:
#             # Invalid signature
#             return JsonResponse({"error": str(e)}, status=400)

#         # Handle the event
#         # Implement your logic based on the event type
#         # For example, update your database, trigger business logic, etc.

#         return JsonResponse({"status": "success"})
