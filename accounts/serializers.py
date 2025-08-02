from rest_framework import serializers
from django.utils import timezone
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'email', 'mobile_number', 'profile_picture',
            'role', 'is_active', 'is_verified', 'date_joined'
        ]

class SendOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

class VerifyOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)
    otp = serializers.IntegerField(min_value=100000, max_value=999999)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    def validate(self, data):
        mobile_number = data['mobile_number']
        otp = str(data['otp'])
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
            raise serializers.ValidationError("Role mismatch.")

        return data
    