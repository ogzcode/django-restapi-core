from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom TokenObtainPairSerializer that includes user data"""
    
    username_field = User.USERNAME_FIELD
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # User bilgilerini ekle
        data['user'] = UserSerializer(self.user).data
        
        return data

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()




