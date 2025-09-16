from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView as SimpleJWTTokenVerifyView,
)

from apps.users.serializers.custom import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)


def make_response(
    success: bool, message: str, data=None, status_code=status.HTTP_200_OK
):
    """Helper function for consistent API responses"""
    return Response(
        {
            "success": success,
            "message": message,
            "data": data or {},
        },
        status=status_code,
    )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view:
    - Issues JWT access & refresh tokens
    - Creates an active session record
    """

    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jwt_token = serializer.validated_data
        refresh_token = jwt_token.get("refresh")
        access_token = jwt_token.get("access")
        user_id = jwt_token.get("user")

        return make_response(
            True,
            "Successfully logged in",
            data={"access": access_token, "refresh": refresh_token, "user": user_id},
        )


class CustomTokenRefreshView(APIView):
    """
    Refresh access token:
    - Validates refresh token
    - Ensures session is active
    - Updates access token JTI
    """

    permission_classes = [AllowAny]
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token_str = serializer.validated_data["refresh"]

        try:
            refresh_token = RefreshToken(refresh_token_str)
            user_id = refresh_token.get("user_id")

            # Create new access token
            new_access_token = str(refresh_token.access_token)

            return make_response(
                True,
                "Successfully refreshed",
                data={
                    "access": str(new_access_token),
                    "refresh": str(refresh_token),
                    "user": user_id,
                },
            )

        except TokenError as e:
            return make_response(
                False,
                "Invalid token",
                data={"error": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return make_response(
                False,
                "Unexpected error",
                data={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomTokenVerifyView(SimpleJWTTokenVerifyView):
    """
    Verify JWT token validity
    """

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            response.data.update({"success": True, "message": "Token is valid"})
            return response
        except InvalidToken as e:
            return make_response(
                False,
                "Token is invalid",
                data={"error": str(e)},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
