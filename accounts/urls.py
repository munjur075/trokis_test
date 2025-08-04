from django.urls import path
from .views import (
    SignupView, send_otp_login, VerifyLoginView, AdminLoginView,
    send_otp, verify_otp, UserProfileView
)

urlpatterns = [
    path('sign-up/', SignupView.as_view(), name='sign-up'),
    path('verify-number/', verify_otp, name='verify-number'),
    path('resend-verification-code/', send_otp, name='resend-verification-code'),

    path('sign-in/', send_otp_login, name='sign-in'),
    path('verify-sign-in/', VerifyLoginView.as_view(), name='verify-sign-in'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('get-user-profile/', UserProfileView.as_view(), name='user_profile'),
]
