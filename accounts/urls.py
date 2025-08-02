from django.urls import path
from .views import (
    SignupView, send_otp_login, VerifyLoginView, AdminLoginView,
    send_otp, verify_otp, UserProfileView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('send-otp-login/', send_otp_login, name='send_otp_login'),
    path('verify-login/', VerifyLoginView.as_view(), name='verify_login'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-number/', verify_otp, name='verify_number'),
    path('get-user-profile/', UserProfileView.as_view(), name='user_profile'),
]
