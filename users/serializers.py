from rest_framework import serializers
from .models import Payment, User
from materials.serializers import CourseSerializer, LessonSerializer
from django.contrib.auth.hashers import make_password


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "avatar", "phone", "city", "payment_history"]

    def get_payment_history(self, obj):
        payments = obj.payments.all().order_by("-payment_date")
        return PaymentSerializer(payments, many=True).data


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2", "phone", "city"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create(
            email=validated_data["email"],
            password=make_password(validated_data["password"]),
            phone=validated_data.get("phone", ""),
            city=validated_data.get("city", ""),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar"]
