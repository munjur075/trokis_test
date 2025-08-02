# models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("Users must have a mobile number")
        
        extra_fields.setdefault("is_active", False)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        return self.create_user(mobile_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('user', 'User'),
        ('guest', 'Guest'),
    )
    mobile_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    otp = models.CharField(max_length=6, blank=True)
    otp_expired = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.mobile_number
    
# views.py
# ----------- views.py -----------
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import random

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import (
    SendOTPSerializer,
    VerifyOTPSerializer,
    UserSerializer
)

# 🔐 Utility to generate a 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)


# ✅ Login via OTP (mobile-based)
class LoginView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            otp = serializer.validated_data['otp']
            role = serializer.validated_data['role']

            try:
                user = User.objects.get(mobile_number=mobile_number)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            if user.otp != otp:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            if user.otp_expired and timezone.now() > user.otp_expired:
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

            if user.role != role:
                return Response({'error': 'Role mismatch. Please login with the correct role.'}, status=status.HTTP_400_BAD_REQUEST)

            # Activate account and clear OTP
            user.is_active = True
            user.otp = None
            user.otp_expired = None
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'status': 'success',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Signup view — sends OTP to new users
class SignupView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            role = serializer.validated_data['role']
            otp = generate_otp()

            if User.objects.filter(mobile_number=mobile_number).exists():
                return Response({'error': 'Mobile number already registered.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(
                mobile_number=mobile_number,
                role=role,
                is_active=False,
                otp=otp,
                otp_expired=timezone.now() + timedelta(minutes=5)
            )
            user.set_password(str(otp))  # optional, for superuser password fallback
            user.save()

            print(f"Sending OTP to {mobile_number}: {otp}")  # ✅ Replace with SMS API

            return Response({
                'status': 'success',
                'message': 'OTP sent to mobile number.',
                'is_new_user': True
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Admin login (mobile/password based)
class AdminLoginView(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')

        if not mobile_number or not password:
            return Response({'error': 'Mobile number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, mobile_number=mobile_number, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_superuser:
            return Response({'error': 'Unauthorized access.'}, status=status.HTTP_403_FORBIDDEN)

        if not user.is_active:
            return Response({'error': 'Account is inactive.'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 'success',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


# ✅ Public: Send OTP (signup or login)
@api_view(['POST'])
def send_otp(request):
    serializer = SendOTPSerializer(data=request.data)
    if serializer.is_valid():
        mobile_number = serializer.validated_data['mobile_number']
        role = serializer.validated_data['role']
        otp = generate_otp()

        user = User.objects.filter(mobile_number=mobile_number).first()

        if user:
            if user.role != role:
                return Response({
                    'error': 'This number is registered with a different role.'
                }, status=status.HTTP_400_BAD_REQUEST)
            created = False
        else:
            user = User.objects.create(
                mobile_number=mobile_number,
                role=role,
                is_active=False
            )
            created = True

        user.otp = otp
        user.otp_expired = timezone.now() + timedelta(minutes=5)
        user.save()

        print(f"Sending OTP to {mobile_number}: {otp}")  # ✅ Replace with real SMS gateway

        return Response({
            'status': 'success',
            'message': 'OTP sent successfully.',
            'is_new_user': created
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Public: Verify OTP and issue JWT tokens
@api_view(['POST'])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        mobile_number = serializer.validated_data['mobile_number']
        otp = serializer.validated_data['otp']
        role = serializer.validated_data['role']

        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp != otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        if user.otp_expired and timezone.now() > user.otp_expired:
            return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        if user.role != role:
            return Response({'error': 'Role mismatch. Please login with the correct role.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.otp = None
        user.otp_expired = None
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 'success',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ✅ Profile view (authenticated users only)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Uncomment if you need update functionality:
    # def put(self, request):
    #     serializer = UserSerializer(request.user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'email',
            'mobile_number',
            'profile_picture',
            'role',
            'is_active',
            'is_guest',
            'date_joined',
        ]


class SendOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20,help_text="Mobile number to send OTP")
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES,help_text="Role of the user (user/driver)")


class VerifyOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20,help_text="Mobile number used during registration/login")
    otp = serializers.IntegerField(min_value=100000,max_value=999999,help_text="6-digit OTP sent to the mobile number")
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES,help_text="Role of the user (user/driver)")

    def validate(self, data):
        mobile_number = data['mobile_number']
        otp = data['otp']
        role = data['role']

        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid mobile number.")

        if user.otp != otp:
            raise serializers.ValidationError("Incorrect OTP.")

        if user.otp_expired and timezone.now() > user.otp_expired:
            raise serializers.ValidationError("OTP has expired.")

        if user.role != role:
            raise serializers.ValidationError("Role mismatch. Please login with the correct role.")

        return data

# admin.py
# ✅ Admin configuration for User model
from django.contrib import admin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('mobile_number','full_name', 'profile_picture','role','email', 'is_active','is_staff','is_superuser')
    # readonly_fields = ('otp',)
    
admin.site.register(User,CustomUserAdmin)


# urls.py
from django.urls import path
from .views import (
    send_otp, verify_otp,
    SignupView, LoginView, AdminLoginView, UserProfileView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-number/', verify_otp, name='verify_number'),
a
    path('get-user-profile/', UserProfileView.as_view(), name='user_profile'),
]