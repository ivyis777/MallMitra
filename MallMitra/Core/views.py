import random
from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import OTPVerification
from .serializer import AdminDriverRegistrationDetailSerializer, LoginOTPSerializer

from .serializer import AdminDriverRegistrationListSerializer
 

from .models import OTPVerification
from .serializer import (
    SendOTPSerializer,
    LoginOTPSerializer,
    ResendOTPSerializer
)


class ConnectionCheckView(APIView):

    def get(self, request):
        return Response({
            "success": True,
            "message": "Connected successfully"
        })


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import SendOTPSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import SendOTPSerializer



import random
from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import OTPVerification
from .serializer import SendOTPSerializer


class ConnectionCheckView(APIView):

    def get(self, request):

        return Response({
            "success": True,
            "message": "Connected successfully"
        })


class SendOTPView(APIView):

    def post(self, request):

        # -----------------------------------------
        # STEP 1: Validate request
        # -----------------------------------------

        serializer = SendOTPSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # STEP 2: Get validated data
        # -----------------------------------------

        mobile_number = serializer.validated_data[
            "mobile_number"
        ]

        channel = serializer.validated_data[
            "channel"
        ]

        # -----------------------------------------
        # STEP 3: Check channel
        # -----------------------------------------

        if channel != "sms":

            return Response(
                {
                    "success": False,
                    "message": "Only SMS channel is supported."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # STEP 4: Generate 4-digit OTP
        # -----------------------------------------

        otp = str(
            random.randint(1000, 9999)
        )

        # -----------------------------------------
        # STEP 5: Set OTP expiry
        # OTP valid for 5 minutes
        # -----------------------------------------

        expires_at = (
            timezone.now()
            + timedelta(minutes=5)
        )

        # -----------------------------------------
        # STEP 6: Save OTP in database
        # -----------------------------------------

        otp_record = OTPVerification.objects.create(

            mobile_number=mobile_number,

            otp=otp,

            channel=channel,

            expires_at=expires_at,

            attempt_count=0
        )

        # -----------------------------------------
        # STEP 7: Print OTP for development
        # -----------------------------------------

        print("\n" + "=" * 60)
        print("             OTP GENERATED")
        print("=" * 60)
        print("Mobile Number  :", mobile_number)
        print("OTP             :", otp)
        print("Verification ID :", otp_record.id)
        print("Channel         :", channel)
        print("Expires At      :", expires_at)
        print("=" * 60 + "\n")

        # -----------------------------------------
        # STEP 8: Return response
        # -----------------------------------------

        return Response(
            {
                "success": True,
                "message": "OTP generated successfully.",
                "mobile_number": mobile_number,
                "channel": channel,
                "verification_id": otp_record.id,
                "expires_at": expires_at,
                "Otp": otp  # For development purposes only. Remove in production.

            },
            status=status.HTTP_200_OK
        )


from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import OTPVerification
from .models import OTPVerification, UserRole


# class LoginOTPView(APIView):

#     def post(self, request):

#         serializer = LoginOTPSerializer(
#             data=request.data
#         )

#         # -----------------------------------
#         # 1. Validate request
#         # -----------------------------------

#         if not serializer.is_valid():

#             return Response(
#                 {
#                     "success": False,
#                     "errors": serializer.errors
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         mobile_number = serializer.validated_data["mobile_number"]
#         otp = serializer.validated_data["otp"]
#         verification_id = serializer.validated_data["verification_id"]
#         channel = serializer.validated_data["channel"]

#         # -----------------------------------
#         # 2. Find OTP using verification ID
#         # -----------------------------------

#         try:

#             otp_record = OTPVerification.objects.get(
#                 id=verification_id,
#                 channel=channel
#             )

#         except OTPVerification.DoesNotExist:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "Invalid verification ID."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------------
#         # 3. Check mobile number
#         # -----------------------------------

#         if otp_record.mobile_number != mobile_number:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "OTP does not match the mobile number."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------------
#         # 4. Check already verified
#         # -----------------------------------

#         if otp_record.verified_at is not None:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "OTP has already been used."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------------
#         # 5. Check OTP expiry
#         # -----------------------------------

#         if timezone.now() > otp_record.expires_at:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "OTP expired."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------------
#         # 6. Check maximum attempts
#         # -----------------------------------

#         if otp_record.attempt_count >= 5:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "Maximum OTP attempts exceeded."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------------
#         # 7. Increase attempt count
#         # -----------------------------------

#         otp_record.attempt_count += 1

#         otp_record.save(
#             update_fields=["attempt_count"]
#         )

#         # -----------------------------------
#         # 8. Check OTP
#         # -----------------------------------

#         if otp_record.otp != otp:

#             return Response(
#                 {
#                     "success": False,
#                     "message": "Invalid OTP."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # -----------------------------------
#         # 9. Mark OTP as verified
#         # -----------------------------------

#         otp_record.verified_at = timezone.now()

#         otp_record.save(
#             update_fields=["verified_at"]
#         )

#         # -----------------------------------
#         # 10. Find UserRole using mobile number
#         # -----------------------------------

#         user_role = UserRole.objects.filter(
#             mobile_number=mobile_number
#         ).first()

#         # -----------------------------------
#         # 11. If mobile number does not exist
#         # -----------------------------------

#         if user_role is None:

#             user_role = UserRole.objects.create(
#                 mobile_number=mobile_number,
#                 is_admin=False,
#                 is_driver=False,
#                 is_truckowner=False,
#                 is_manufacturer=False,
#                 is_transport_vendor=False
#             )

#         # -----------------------------------
#         # 12. Get approved roles
#         # -----------------------------------

#         roles = []

#         if user_role.is_admin:
#             roles.append("admin")

#         if user_role.is_driver:
#             roles.append("driver")

#         if user_role.is_truckowner:
#             roles.append("truckowner")

#         if user_role.is_manufacturer:
#             roles.append("manufacturer")

#         if user_role.is_transport_vendor:
#             roles.append("transport_vendor")

#         # -----------------------------------
#         # 13. Decide next screen
#         # -----------------------------------

#         if len(roles) == 0:

#             next_screen = "role_selection"

#         elif len(roles) == 1:

#             next_screen = f"{roles[0]}_home"

#         else:

#             next_screen = "role_selection"

#         # -----------------------------------
#         # 14. Login successful
#         # -----------------------------------

#         print(
#             "OTP VERIFIED:",
#             mobile_number
#         )

#         print(
#             "ROLES:",
#             roles
#         )

#         return Response(
#             {
#                 "success": True,
#                 "message": "OTP verified successfully. Login successful.",

#                 "mobile_number": mobile_number,

#                 "verification_id": verification_id,

#                 "roles": roles,

#                 "next_screen": next_screen
#             },
#             status=status.HTTP_200_OK
#         )

class LoginOTPView(APIView):

    def post(self, request):

        serializer = LoginOTPSerializer(
            data=request.data
        )

        # -----------------------------------
        # 1. Validate request
        # -----------------------------------

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        mobile_number = serializer.validated_data["mobile_number"]
        otp = serializer.validated_data["otp"]
        verification_id = serializer.validated_data["verification_id"]
        channel = serializer.validated_data["channel"]

        # -----------------------------------
        # 2. Find OTP
        # -----------------------------------

        try:

            otp_record = OTPVerification.objects.get(
                id=verification_id,
                channel=channel
            )

        except OTPVerification.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Invalid verification ID."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 3. Check mobile number
        # -----------------------------------

        if otp_record.mobile_number != mobile_number:

            return Response(
                {
                    "success": False,
                    "message": "OTP does not match the mobile number."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 4. Check already verified
        # -----------------------------------

        if otp_record.verified_at is not None:

            return Response(
                {
                    "success": False,
                    "message": "OTP has already been used."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 5. Check expiry
        # -----------------------------------

        if timezone.now() > otp_record.expires_at:

            return Response(
                {
                    "success": False,
                    "message": "OTP expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 6. Check maximum attempts
        # -----------------------------------

        if otp_record.attempt_count >= 5:

            return Response(
                {
                    "success": False,
                    "message": "Maximum OTP attempts exceeded."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 7. Increase attempt count
        # -----------------------------------

        otp_record.attempt_count += 1

        otp_record.save(
            update_fields=["attempt_count"]
        )

        # -----------------------------------
        # 8. Check OTP
        # -----------------------------------

        if otp_record.otp != otp:

            return Response(
                {
                    "success": False,
                    "message": "Invalid OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 9. Mark OTP as verified
        # -----------------------------------

        otp_record.verified_at = timezone.now()

        otp_record.save(
            update_fields=["verified_at"]
        )

        # -----------------------------------
        # 10. Find or create UserRole
        # -----------------------------------

        user_role, created = UserRole.objects.get_or_create(
            mobile_number=mobile_number,
            defaults={
                "is_admin": False,
                "is_driver": False,
                "is_truckowner": False,
                "is_manufacturer": False,
                "is_transport_vendor": False
            }
        )

        # -----------------------------------
        # 11. Get approved roles
        # -----------------------------------

        roles = []

        if user_role.is_admin:
            roles.append("admin")

        if user_role.is_driver:
            roles.append("driver")

        if user_role.is_truckowner:
            roles.append("truckowner")

        if user_role.is_manufacturer:
            roles.append("manufacturer")

        if user_role.is_transport_vendor:
            roles.append("transport_vendor")

        # -----------------------------------
        # 12. Decide next screen
        # -----------------------------------

        if len(roles) == 0:

            next_screen = "role_selection"

        elif len(roles) == 1:

            next_screen = f"{roles[0]}_home"

        else:

            next_screen = "role_selection"

        # -----------------------------------
        # 13. Create Refresh Token
        # -----------------------------------

        refresh = RefreshToken()

        # -----------------------------------
        # 14. Add custom claims
        # -----------------------------------

        refresh["mobile_number"] = mobile_number
        refresh["roles"] = roles

        # -----------------------------------
        # 15. Create Access Token
        # -----------------------------------

        access_token = refresh.access_token

        access_token["mobile_number"] = mobile_number
        access_token["roles"] = roles

        # -----------------------------------
        # 16. Login successful
        # -----------------------------------

        print(
            "OTP VERIFIED:",
            mobile_number
        )

        print(
            "ROLES:",
            roles
        )

        return Response(
            {
                "success": True,
                "message": "OTP verified successfully. Login successful.",

                "mobile_number": mobile_number,

                "verification_id": verification_id,

                "roles": roles,

                "next_screen": next_screen,

                "access_token": str(access_token),

                "refresh_token": str(refresh)
            },
            status=status.HTTP_200_OK
        )

    
class ResendOTPView(APIView):

    def post(self, request):

        # -----------------------------------
        # 1. Validate request
        # -----------------------------------

        serializer = ResendOTPSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        mobile_number = serializer.validated_data["mobile_number"]
        verification_id = serializer.validated_data["verification_id"]
        channel = serializer.validated_data["channel"]

        # -----------------------------------
        # 2. Find existing OTP
        # -----------------------------------

        try:

            old_otp_record = OTPVerification.objects.get(
                id=verification_id,
                channel=channel
            )

        except OTPVerification.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Invalid verification ID."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 3. Check mobile number
        # -----------------------------------

        if old_otp_record.mobile_number != mobile_number:

            return Response(
                {
                    "success": False,
                    "message": "OTP does not match the mobile number."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 4. Generate new OTP
        # -----------------------------------

        new_otp = str(
            random.randint(1000, 9999)
        )

        new_expires_at = (
            timezone.now() + timedelta(seconds=30)
        )

        # -----------------------------------
        # 5. Expire old OTP
        # -----------------------------------

        old_otp_record.expires_at = timezone.now()

        old_otp_record.save(
            update_fields=["expires_at"]
        )

        # -----------------------------------
        # 6. Create new OTP
        # -----------------------------------

        new_otp_record = OTPVerification.objects.create(
            mobile_number=mobile_number,
            otp=new_otp,
            channel=channel,
            expires_at=new_expires_at,
            attempt_count=0
        )

        # -----------------------------------
        # 7. Print OTP for development
        # -----------------------------------

        print("=" * 60)
        print("OTP RESENT")
        print("Mobile Number  :", mobile_number)
        print("NEW OTP        :", new_otp)
        print("Verification ID:", new_otp_record.id)
        print("Expires At     :", new_expires_at)
        print("=" * 60)

        # -----------------------------------
        # 8. Return response
        # -----------------------------------

        return Response(
            {
                "success": True,
                "message": "OTP resent successfully.",
                "mobile_number": mobile_number,
                "channel": channel,
                "verification_id": new_otp_record.id,
                "expires_at": new_expires_at,
                "Otp": new_otp  # For development purposes only. Remove in production.
            },
            status=status.HTTP_200_OK
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializer import CompanySerializer


class CompanyCreateView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():

            company = serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Company added successfully",
                    "data": CompanySerializer(company).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "message": "Company creation failed",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DriverRegistration, Company
from .serializer import DriverRegistrationSerializer


class DriverRegistrationView(APIView):

    def post(self, request):

        # =========================================
        # GET MOBILE NUMBER
        # =========================================

        mobile_number = request.data.get(
            "mobile_number"
        )

        if not mobile_number:

            return Response(
                {
                    "success": False,
                    "message": "Mobile number is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =========================================
        # CHECK EXISTING DRIVER REGISTRATION
        # =========================================

        existing_registration = (
            DriverRegistration.objects.filter(
                mobile_number=mobile_number
            ).first()
        )

        if existing_registration:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Driver registration already exists "
                        "for this mobile number."
                    ),
                    "registration_id": (
                        existing_registration.id
                    ),
                    "status": (
                        existing_registration.status
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =========================================
        # GET IVYIS COMPANY
        # =========================================

        ivyis_company = (
            Company.objects.filter(
                company_name__iexact="Ivyis Technologies"
            ).first()
        )

        # =========================================
        # SERIALIZER
        # =========================================

        serializer = DriverRegistrationSerializer(
            data=request.data,
            context={
                "ivyis_company": ivyis_company
            }
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": (
                        "Driver registration failed."
                    ),
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =========================================
        # CREATE DRIVER REGISTRATION
        # =========================================

        driver = serializer.save()

        return Response(
            {
                "success": True,
                "message": (
                    "Driver registration submitted "
                    "successfully. Waiting for admin approval."
                ),
                "registration_id": driver.id,
                "mobile_number": driver.mobile_number,
                "company": driver.company.company_name,
                "status": driver.status
            },
            status=status.HTTP_201_CREATED
        )

from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
class AdminApproveDriverView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, registration_id):

        # -----------------------------------
        # 1. Check logged-in admin
        # -----------------------------------

        admin_role = request.user

        if not admin_role.is_admin:

            return Response(
                {
                    "success": False,
                    "message": "Admin access required."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -----------------------------------
        # 2. Find driver registration
        # -----------------------------------

        try:

            driver = DriverRegistration.objects.get(
                id=registration_id
            )

        except DriverRegistration.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Driver registration not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -----------------------------------
        # 3. Check pending status
        # -----------------------------------

        if driver.status != "pending":

            return Response(
                {
                    "success": False,
                    "message": f"Driver registration is already {driver.status}."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 4. Approve driver
        # -----------------------------------

        driver.status = "approved"
        driver.reviewed_at = timezone.now()
        driver.rejection_reason = None

        driver.save(
            update_fields=[
                "status",
                "reviewed_at",
                "rejection_reason",
                "updated_at"
            ]
        )

        # -----------------------------------
        # 5. Find or create UserRole
        # -----------------------------------

        user_role, created = UserRole.objects.get_or_create(
            mobile_number=driver.mobile_number
        )

        # -----------------------------------
        # 6. Activate Driver role
        # -----------------------------------

        user_role.is_driver = True

        user_role.save(
            update_fields=[
                "is_driver",
                "updated_at"
            ]
        )

        # -----------------------------------
        # 7. Success response
        # -----------------------------------

        return Response(
            {
                "success": True,
                "message": "Driver registration approved successfully.",
                "registration_id": driver.id,
                "mobile_number": driver.mobile_number,
                "status": driver.status,
                "is_driver": user_role.is_driver
            },
            status=status.HTTP_200_OK
        )

class AdminDriverRegistrationListView(APIView):

    def get(self, request):

        # -----------------------------------
        # 1. Fetch ALL driver registrations
        # -----------------------------------

        registrations = DriverRegistration.objects.select_related(
            "company"
        ).order_by(
            "-created_at"
        )

        # -----------------------------------
        # 2. Serialize
        # -----------------------------------

        serializer = AdminDriverRegistrationListSerializer(
            registrations,
            many=True
        )

        # -----------------------------------
        # 3. Separate by status
        # -----------------------------------

        pending = []
        approved = []
        rejected = []

        for driver in serializer.data:

            if driver["status"] == "pending":

                pending.append(driver)

            elif driver["status"] == "approved":

                approved.append(driver)

            elif driver["status"] == "rejected":

                rejected.append(driver)

        # -----------------------------------
        # 4. Return response
        # -----------------------------------

        return Response(
            {
                "success": True,
                "message": "Driver registrations fetched successfully.",

                "summary": {
                    "total": len(serializer.data),
                    "pending": len(pending),
                    "approved": len(approved),
                    "rejected": len(rejected)
                },

                "pending": pending,

                "approved": approved,

                "rejected": rejected
            },
            status=status.HTTP_200_OK
        )
    

from rest_framework.permissions import IsAuthenticated
class AdminDriverRegistrationDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, registration_id):

        # -----------------------------------
        # 1. Get authenticated admin
        # -----------------------------------

        user_role = request.user

        # -----------------------------------
        # 2. Check admin permission
        # -----------------------------------

        if not user_role.is_admin:

            return Response(
                {
                    "success": False,
                    "message": "Admin access required."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -----------------------------------
        # 3. Find driver registration
        # -----------------------------------

        try:

            driver = DriverRegistration.objects.select_related(
                "company"
            ).get(
                id=registration_id
            )

        except DriverRegistration.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Driver registration not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -----------------------------------
        # 4. Serialize complete details
        # -----------------------------------

        serializer = AdminDriverRegistrationDetailSerializer(
            driver
        )

        # -----------------------------------
        # 5. Return response
        # -----------------------------------

        return Response(
            {
                "success": True,
                "message": "Driver registration details fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

#Admmin Reject
class AdminRejectDriverView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, registration_id):

        # -----------------------------------
        # 1. Check logged-in admin
        # -----------------------------------

        admin_role = request.user

        if not admin_role.is_admin:

            return Response(
                {
                    "success": False,
                    "message": "Admin access required."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -----------------------------------
        # 2. Get rejection reason
        # -----------------------------------

        rejection_reason = request.data.get("rejection_reason")

        if not rejection_reason:

            return Response(
                {
                    "success": False,
                    "message": "Rejection reason is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        rejection_reason = rejection_reason.strip()

        if not rejection_reason:

            return Response(
                {
                    "success": False,
                    "message": "Rejection reason cannot be empty."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 3. Find driver registration
        # -----------------------------------

        try:

            driver = DriverRegistration.objects.get(
                id=registration_id
            )

        except DriverRegistration.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Driver registration not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -----------------------------------
        # 4. Check pending status
        # -----------------------------------

        if driver.status != "pending":

            return Response(
                {
                    "success": False,
                    "message": f"Driver registration is already {driver.status}."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 5. Reject driver
        # -----------------------------------

        driver.status = "rejected"
        driver.rejection_reason = rejection_reason
        driver.reviewed_at = timezone.now()

        driver.save(
            update_fields=[
                "status",
                "rejection_reason",
                "reviewed_at",
                "updated_at"
            ]
        )

        # -----------------------------------
        # 6. Find or create UserRole
        # -----------------------------------

        user_role, created = UserRole.objects.get_or_create(
            mobile_number=driver.mobile_number
        )

        # -----------------------------------
        # 7. Keep Driver role inactive
        # -----------------------------------

        user_role.is_driver = False

        user_role.save(
            update_fields=[
                "is_driver",
                "updated_at"
            ]
        )

        # -----------------------------------
        # 8. Success response
        # -----------------------------------

        return Response(
            {
                "success": True,
                "message": "Driver registration rejected successfully.",
                "registration_id": driver.id,
                "mobile_number": driver.mobile_number,
                "status": driver.status,
                "rejection_reason": driver.rejection_reason,
                "is_driver": user_role.is_driver
            },
            status=status.HTTP_200_OK
        )


# driver profile view
class DriverProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # -----------------------------------
        # 1. Get authenticated user
        # -----------------------------------

        user_role = request.user

        # -----------------------------------
        # 2. Check Driver role
        # -----------------------------------

        if not user_role.is_driver:

            return Response(
                {
                    "success": False,
                    "message": "Driver access required."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -----------------------------------
        # 3. Get driver's mobile number
        # -----------------------------------

        mobile_number = user_role.mobile_number

        # -----------------------------------
        # 4. Find approved driver registration
        # -----------------------------------

        try:

            driver = DriverRegistration.objects.select_related(
                "company"
            ).get(
                mobile_number=mobile_number,
                status="approved"
            )

        except DriverRegistration.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Approved driver registration not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -----------------------------------
        # 5. Serialize driver details
        # -----------------------------------

        serializer = AdminDriverRegistrationDetailSerializer(
            driver
        )

        # -----------------------------------
        # 6. Return response
        # -----------------------------------

        return Response(
            {
                "success": True,
                "message": "Driver profile fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )