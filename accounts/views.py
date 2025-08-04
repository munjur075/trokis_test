from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import SendOTPSerializer, VerifyOTPSerializer, UserSerializer
import random

def generate_otp():
    return str(random.randint(100000, 999999))

class SignupView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            role = serializer.validated_data['role']

            # Only allow 'user' or 'driver' roles during signup
            if role not in ['user', 'driver']:
                return Response({"message": "Invalid role. Must be 'user' or 'driver''."}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(mobile_number=mobile_number).exists():
                return Response({"message": "Mobile number already registered."}, status=status.HTTP_400_BAD_REQUEST)

            otp = generate_otp()
            user = User.objects.create(
                mobile_number=mobile_number,
                role=role,
                otp=otp,
                otp_expired=timezone.now() + timedelta(minutes=5)
            )
            user.set_password(otp)
            user.save()

            print(f"OTP sent to {mobile_number}: {otp}")

            return Response({
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_otp_login(request):
    serializer = SendOTPSerializer(data=request.data)
    if serializer.is_valid():
        mobile_number = serializer.validated_data['mobile_number']
        # print(serializer.validated_data)
        # role = serializer.validated_data['role']

        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return Response({"message": 'User not registered'}, status=status.HTTP_404_NOT_FOUND)

        # if user.role != role:
        #     return Response({"message": 'Role mismatch'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active or not user.is_verified:
            return Response({"message": 'User is not active or verified. Please active or verified first'}, status=status.HTTP_403_FORBIDDEN)

        otp = generate_otp()
        user.otp = otp
        user.otp_expired = timezone.now() + timedelta(minutes=5)
        user.save()

        print(f"Sending login OTP to {mobile_number}: {otp}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyLoginView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            otp = str(serializer.validated_data['verification_code'])
            # role = serializer.validated_data['role']

            try:
                user = User.objects.get(mobile_number=mobile_number)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            if user.otp != otp:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            if user.otp_expired and timezone.now() > user.otp_expired:
                return Response({"message": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

            # if user.role != role:
            #     return Response({"message": 'Role mismatch'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.otp = None
            user.otp_expired = None
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user_id': user.id,
                "role": user.role
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginView(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')

        if not mobile_number or not password:
            return Response({"message": 'Mobile number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, mobile_number=mobile_number, password=password)
        if not user or not user.is_superuser:
            return Response({"message": 'Invalid credentials or unauthorized access.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({"message": 'Account is inactive.'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'success',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def send_otp(request):
    serializer = SendOTPSerializer(data=request.data)
    if serializer.is_valid():
        mobile_number = serializer.validated_data['mobile_number']
        # print(serializer.validated_data)
        # role = serializer.validated_data['role']

        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return Response({"message": "User not registered"}, status=status.HTTP_404_NOT_FOUND)

        # if user.role != role:
        #     return Response({"message": "Role mismatch"}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        user.otp = otp
        user.otp_expired = timezone.now() + timedelta(minutes=5)
        user.save()

        print(f"Sending verification-code to {mobile_number}: {otp}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    
    if serializer.is_valid():
        mobile_number = serializer.validated_data['mobile_number']
        otp = str(serializer.validated_data['verification_code'])

        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return Response({"message": 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Check if already verified (optional handling)
        if user.is_verified:
            return Response({"message": "User already verified."}, status=status.HTTP_200_OK)

        # ❌ Wrong OTP
        if user.otp != otp:
            return Response({"message": 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

        # ⏰ OTP Expired
        if user.otp_expired and timezone.now() > user.otp_expired:
            return Response({"message": 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Success
        user.is_active = True
        user.is_verified = True
        user.otp = None
        user.otp_expired = None
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user_id": user.id,
            "role": user.role
        }, status=status.HTTP_200_OK)

    # ❌ Invalid Input
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
