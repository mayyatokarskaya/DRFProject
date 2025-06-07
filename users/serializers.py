from rest_framework import serializers
from .models import Payment, User
from materials.serializers import CourseSerializer, LessonSerializer


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'phone', 'city', 'payment_history']

    def get_payment_history(self, obj):
        payments = obj.payments.all().order_by('-payment_date')
        return PaymentSerializer(payments, many=True).data
