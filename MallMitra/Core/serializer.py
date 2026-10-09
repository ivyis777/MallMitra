from rest_framework import serializers
from .models import OTPVerification


from rest_framework import serializers
from .models import OTPVerification


class SendOTPSerializer(serializers.Serializer):

    mobile_number = serializers.CharField(
        min_length=10,
        max_length=10
    )

    channel = serializers.ChoiceField(
        choices=OTPVerification.CHANNEL_CHOICES
    )

    def validate_mobile_number(self, value):

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        if value[0] not in "6789":
            raise serializers.ValidationError(
                "Enter a valid Indian mobile number."
            )

        return value


class LoginOTPSerializer(serializers.Serializer):

    mobile_number = serializers.CharField(
        min_length=10,
        max_length=10
    )

    otp = serializers.CharField(
        min_length=4,
        max_length=4
    )

    verification_id = serializers.IntegerField(
        required=True
    )

    channel = serializers.ChoiceField(
        choices=OTPVerification.CHANNEL_CHOICES
    )

    def validate_mobile_number(self, value):

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        if value[0] not in "6789":
            raise serializers.ValidationError(
                "Enter a valid Indian mobile number."
            )

        return value

    def validate_otp(self, value):

        if not value.isdigit():
            raise serializers.ValidationError(
                "OTP must contain only digits."
            )

        return value


from rest_framework import serializers
from .models import OTPVerification


from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import OTPVerification


class LoginOTPView(APIView):

    def post(self, request):

        # -----------------------------------------
        # STEP 1: Validate request
        # -----------------------------------------

        serializer = LoginOTPSerializer(
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

        mobile_number = serializer.validated_data["mobile_number"]
        otp = serializer.validated_data["otp"]
        verification_id = serializer.validated_data["verification_id"]
        channel = serializer.validated_data["channel"]

        # -----------------------------------------
        # STEP 3: Find OTP using verification ID
        # -----------------------------------------

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

        # -----------------------------------------
        # STEP 4: Check mobile number
        # -----------------------------------------

        if otp_record.mobile_number != mobile_number:

            return Response(
                {
                    "success": False,
                    "message": "OTP does not match the mobile number."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # STEP 5: Check if OTP already verified
        # -----------------------------------------

        if otp_record.verified_at is not None:

            return Response(
                {
                    "success": False,
                    "message": "OTP has already been used."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # STEP 6: Check OTP expiry
        # -----------------------------------------

        if timezone.now() > otp_record.expires_at:

            return Response(
                {
                    "success": False,
                    "message": "OTP expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # STEP 7: Check maximum attempts
        # -----------------------------------------

        if otp_record.attempt_count >= 5:

            return Response(
                {
                    "success": False,
                    "message": "Maximum OTP attempts exceeded."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # STEP 8: Increase attempt count
        # -----------------------------------------

        otp_record.attempt_count += 1

        otp_record.save(
            update_fields=["attempt_count"]
        )

        # -----------------------------------------
        # STEP 9: Check OTP
        # -----------------------------------------

        if otp_record.otp != otp:

            return Response(
                {
                    "success": False,
                    "message": "Invalid OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # STEP 10: Mark OTP as verified
        # -----------------------------------------

        otp_record.verified_at = timezone.now()

        otp_record.save(
            update_fields=["verified_at"]
        )

        # -----------------------------------------
        # STEP 11: Login successful
        # -----------------------------------------

        print(
            "OTP VERIFIED:",
            mobile_number
        )

        return Response(
            {
                "success": True,
                "message": "OTP verified successfully. Login successful.",
                "mobile_number": mobile_number,
                "verification_id": verification_id
            },
            status=status.HTTP_200_OK
        )


    # Resend Otp Serializer
class ResendOTPSerializer(serializers.Serializer):

    mobile_number = serializers.CharField(
        min_length=10,
        max_length=10
    )

    verification_id = serializers.IntegerField(
        required=True
    )

    channel = serializers.ChoiceField(
        choices=OTPVerification.CHANNEL_CHOICES
    )

    def validate_mobile_number(self, value):

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        if value[0] not in "6789":
            raise serializers.ValidationError(
                "Enter a valid Indian mobile number."
            )

        return value
    

from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

        fields = [
            "company_id",
            "company_uniqueid",
            "company_name",
            "gst_number",
            "email",
            "phone_number",
            "company_person_number",
            "address",
            "city",
            "state",
            "pincode",
            "country",
            "document_type",
            "document",
            "other_document",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "company_id",
            "created_at",
            "updated_at",
        ]

from rest_framework import serializers
from .models import DriverRegistration


class DriverRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverRegistration

        fields = [
            # Company
            "company_type",
            "company",

            # Personal Details
            "name",
            "age",
            "gender",
            "mobile_number",

            # Aadhaar
            "aadhaar_number",

            # Driving Licence
            "driving_licence_number",
            "dl_type",
            "dl_issued_date",
            "dl_expired_date",

            # Address
            "permanent_address",
            "current_address",

            # Documents
            "medical_certificate",
            "police_verification_certificate",
            "photo",
            "aadhaar_front",
            "aadhaar_back",
            "dl_front",
            "dl_back",
        ]

        read_only_fields = [
            "status",
            "rejection_reason",
            "reviewed_at",
        ]

    # -------------------------
    # Mobile Number
    # -------------------------

    def validate_mobile_number(self, value):

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        if value[0] not in "6789":
            raise serializers.ValidationError(
                "Enter a valid Indian mobile number."
            )

        return value

    # -------------------------
    # Aadhaar
    # -------------------------

    def validate_aadhaar_number(self, value):

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Aadhaar number must contain only digits."
            )

        if len(value) != 12:
            raise serializers.ValidationError(
                "Aadhaar number must contain exactly 12 digits."
            )

        return value

    # -------------------------
    # Age
    # -------------------------

    def validate_age(self, value):

        if value < 18:
            raise serializers.ValidationError(
                "Driver must be at least 18 years old."
            )

        if value > 100:
            raise serializers.ValidationError(
                "Enter a valid age."
            )

        return value

    # -------------------------
    # Medical Certificate
    # PDF only
    # -------------------------

    def validate_medical_certificate(self, value):

        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Medical certificate must be a PDF file."
            )

        return value

    # -------------------------
    # Police Verification
    # PDF only
    # -------------------------

    def validate_police_verification_certificate(
        self,
        value
    ):

        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Police verification certificate must be a PDF file."
            )

        return value

    # -------------------------
    # Complete Validation
    # -------------------------

    def validate(self, attrs):

        company_type = attrs.get("company_type")
        company = attrs.get("company")

        # =========================
        # IVYIS
        # =========================

        if company_type == "ivyis":

            ivyis_company = (
                self.context.get("ivyis_company")
            )

            if not ivyis_company:
                raise serializers.ValidationError({
                    "company": (
                        "IVYIS company is not configured."
                    )
                })

            attrs["company"] = ivyis_company

        # =========================
        # OTHER COMPANY
        # =========================

        elif company_type == "other":

            if not company:
                raise serializers.ValidationError({
                    "company": (
                        "Please select an existing company."
                    )
                })

        return attrs

#Get API
class AdminDriverRegistrationListSerializer(serializers.ModelSerializer):

    company_name = serializers.SerializerMethodField()

    class Meta:
        model = DriverRegistration

        fields = [
            "id",
            "name",
            "age",
            "gender",
            "mobile_number",
            "company_type",
            "company_name",
            "driving_licence_number",
            "dl_type",
            "status",
            "created_at",
        ]

    def get_company_name(self, obj):

        if obj.company:
            return obj.company.company_name

        return "Ivyis Technologies"

#Driver Registration Details

class AdminDriverRegistrationDetailSerializer(serializers.ModelSerializer):

    company_name = serializers.SerializerMethodField()

    class Meta:
        model = DriverRegistration

        fields = [
            "id",

            # Company
            "company_type",
            "company_name",

            # Personal details
            "name",
            "age",
            "gender",
            "mobile_number",
            "aadhaar_number",

            # Driving licence
            "driving_licence_number",
            "dl_type",
            "dl_issued_date",
            "dl_expired_date",

            # Address
            "permanent_address",
            "current_address",

            # Documents
            "medical_certificate",
            "police_verification_certificate",

            "photo",

            "aadhaar_front",
            "aadhaar_back",

            "dl_front",
            "dl_back",

            # Status
            "status",
            "rejection_reason",
            "reviewed_at",

            # Dates
            "created_at",
            "updated_at",
        ]

    def get_company_name(self, obj):

        if obj.company:
            return obj.company.company_name

        return "Ivyis Technologies"