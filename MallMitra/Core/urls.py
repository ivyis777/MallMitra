from django.urls import path
from .views import ConnectionCheckView, SendOTPView

urlpatterns = [
    path("send-otp/",SendOTPView.as_view(),name="send-otp"),
    path("connection/", ConnectionCheckView.as_view(), name="connection"),
]