from rest_framework import serializers
from .models import OTPVerification


class SendOTPSerializer(serializers.Serializer):

    mobile_number = serializers.CharField(
        max_length=13,
        min_length=13
    )

    channel = serializers.ChoiceField(
        choices=OTPVerification.CHANNEL_CHOICES
    )

    def validate_mobile_number(self, value):
        value = value.strip()

        # Must start with India's country code
        if not value.startswith("+91"):
            raise serializers.ValidationError(
                "Mobile number must start with +91."
            )

        # Get the 10-digit number after +91
        mobile = value[3:]

        if not mobile.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits after +91."
            )

        if len(mobile) != 10:
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number after +91."
            )

        # Return complete number with country code
        return value