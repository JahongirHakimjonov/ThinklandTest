from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models.users import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email_number_field = "email"

    def validate(self, attrs):
        credentials = {
            "email": attrs.get(self.email_number_field),
            "password": attrs.get("password"),
        }

        user = User.objects.filter(email=credentials["email"]).first()
        if user:
            user = authenticate(email=user.email, password=credentials["password"])

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        token = super().get_token(user)

        token["email"] = user.email

        return {
            "refresh": str(token),
            "access": str(token.access_token),
            "user": user.id,
        }


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get("refresh")

        if refresh is None:
            raise serializers.ValidationError("No refresh token provided")

        return {"refresh": refresh}
