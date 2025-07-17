from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import (
    RegisterSerializer,
    LoginResponseSerializer,
    TokenRefreshResponseSerializer,
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        tags=['Auth'],
        summary='Login',
        description='Login with username/email and password',
        auth=[],
        responses={200: LoginResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(
        tags=['Auth'],
        summary='Refresh Token',
        description='Refresh access token using refresh token',
        auth=[],
        responses={200: TokenRefreshResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Auth'],
        summary='Register',
        description='Register a new user account',
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description='User created successfully'),
            400: OpenApiResponse(description='Validation errors')
        },
        auth=[]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"message": "User created successfully"},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to create user"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
