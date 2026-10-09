from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import UserRole


class MobileJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        # -----------------------------------
        # 1. Get Authorization header
        # -----------------------------------

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        # -----------------------------------
        # 2. Check Bearer token
        # -----------------------------------

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":

            raise AuthenticationFailed(
                "Invalid Authorization header."
            )

        token = parts[1]

        # -----------------------------------
        # 3. Validate access token
        # -----------------------------------

        try:

            access_token = AccessToken(token)

        except TokenError:

            raise AuthenticationFailed(
                "Invalid or expired access token."
            )

        # -----------------------------------
        # 4. Get mobile number from token
        # -----------------------------------

        mobile_number = access_token.get(
            "mobile_number"
        )

        if not mobile_number:

            raise AuthenticationFailed(
                "Mobile number not found in token."
            )

        # -----------------------------------
        # 5. Find UserRole
        # -----------------------------------

        try:

            user_role = UserRole.objects.get(
                mobile_number=mobile_number
            )

        except UserRole.DoesNotExist:

            raise AuthenticationFailed(
                "User role not found."
            )

        # -----------------------------------
        # 6. Return authenticated user
        # -----------------------------------

        return (
            user_role,
            access_token
        )