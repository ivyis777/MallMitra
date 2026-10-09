from django.urls import path
from .views import AdminDriverRegistrationListView, ConnectionCheckView, DriverProfileView, SendOTPView,ResendOTPView
from .views import LoginOTPView
from .views import CompanyCreateView
from .views import DriverRegistrationView
from .views import AdminApproveDriverView
from .views import AdminDriverRegistrationListView

from .views import AdminDriverRegistrationDetailView
from .views import AdminRejectDriverView

urlpatterns = [
    path("send-otp/",SendOTPView.as_view(),name="send-otp"),
    path("login/",LoginOTPView.as_view(),name="login-otp"),
    path("resend-otp/",ResendOTPView.as_view(),name="resend-otp"),

     #Driver Registration
    path("driver/register/",DriverRegistrationView.as_view(),name="driver-register"),
    path("admin/drivers/",AdminDriverRegistrationListView.as_view(),name="admin-driver-registrations"),
    path("admin/drivers/<int:registration_id>/",AdminDriverRegistrationDetailView.as_view(),name="admin-driver-registration-detail"),
    path("admin/drivers/<int:registration_id>/approve/",AdminApproveDriverView.as_view(),name="admin-approve-driver"),
    path("admin/drivers/<int:registration_id>/reject/",AdminRejectDriverView.as_view(),name="admin-reject-driver"),
    path("driver/profile/",DriverProfileView.as_view(),name="driver-profile"),


    #add Company 
    path("company/add/", CompanyCreateView.as_view(), name="company-add"),


    path("connection/", ConnectionCheckView.as_view(), name="connection"),
]