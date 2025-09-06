from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from materials.models import Course
from .models import Payment
from .services.stripe_service import create_stripe_product, create_stripe_price, create_checkout_session

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        product_id = create_stripe_product(course.title)
        price_id = create_stripe_price(product_id, int(course.price * 100))

        success_url = "http://localhost:8000/success"
        cancel_url = "http://localhost:8000/cancel"

        session = create_checkout_session(price_id, success_url, cancel_url)

        Payment.objects.create(
            user=request.user,
            course=course,
            stripe_session_id=session.id,
            stripe_payment_url=session.url
        )

        return Response({"checkout_url": session.url})

