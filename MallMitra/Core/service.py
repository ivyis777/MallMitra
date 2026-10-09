# import base64
# import requests
# import logging
# from django.conf import settings

# logger = logging.getLogger(__name__)

# BASE_URL = "https://cpaas.messagecentral.com"


# def get_auth_token():
#     key = base64.b64encode(
#         settings.MESSAGE_CENTRAL_PASSWORD.encode()
#     ).decode()

#     response = requests.get(
#         f"{BASE_URL}/auth/v1/authentication/token",
#         params={
#             "country": "IN",
#             "customerId": settings.MESSAGE_CENTRAL_CUSTOMER_ID,
#             "key": key,
#             "scope": "NEW",
#         },
#         timeout=15,
#     )
#     print("TOKEN RESPONSE:", response.status_code, response.text)
#     response.raise_for_status()
#     return response.json()["token"]


# def send_sms_otp(mobile_number: str):
#     """Send OTP through Message Central."""

#     try:
#         token = get_auth_token()

#         # Remove +91 before sending to Message Central
#         mobile_number = str(mobile_number).strip()

#         if mobile_number.startswith("+91"):
#             mobile_number = mobile_number[3:]

#         response = requests.post(
#             f"{BASE_URL}/verification/v3/send",
#             params={
#                 "countryCode": "91",
#                 "customerId": settings.MESSAGE_CENTRAL_CUSTOMER_ID,
#                 "flowType": "SMS",
#                 "mobileNumber": mobile_number,
#                 "otpLength": 4,
#             },
#             headers={
#                 "authToken": token
#             },
#             timeout=15,
#         )

#         print("SEND RESPONSE:", response.status_code, response.text)

#         if response.status_code == 200:
#             data = response.json()

#             if str(data.get("responseCode")) == "200":
#                 return data["data"]["verificationId"]

#         return None

#     except (requests.exceptions.RequestException, KeyError) as e:
#         print("Message Central error:", e)
#         return None
# def send_sms_otp(mobile_number: str):
#     """Send OTP through Message Central."""

#     try:
#         token = get_auth_token()

#         mobile_number = str(mobile_number).strip()

#         if mobile_number.startswith("+91"):
#             mobile_number = mobile_number[3:]

#         response = requests.post(
#             f"{BASE_URL}/verification/v3/send",
#             params={
#                 "countryCode": "91",
#                 "customerId": settings.MESSAGE_CENTRAL_CUSTOMER_ID,
#                 "flowType": "SMS",
#                 "mobileNumber": mobile_number,
#                 "otpLength": 4,
#             },
#             headers={
#                 "authToken": token
#             },
#             timeout=15,
#         )

#         print("SEND RESPONSE:", response.status_code, response.text)

#         if response.status_code == 200:
#             data = response.json()

#             print("FULL OTP RESPONSE:", data)

#             if str(data.get("responseCode")) == "200":

#                 verification_id = data["data"]["verificationId"]

#                 otp = data["data"].get("otp")

#                 return {
#                     "verification_id": verification_id,
#                     "otp": otp
#                 }

#         return None

#     except (requests.exceptions.RequestException, KeyError) as e:
#         print("Message Central error:", e)
#         return None


# def validate_sms_otp(mobile_number: str, verification_id: str, code: str) -> bool:
#     try:
#         token = get_auth_token()
#         response = requests.get(
#             f"{BASE_URL}/verification/v3/validateOtp",
#             params={
#                 "countryCode": "91",
#                 "mobileNumber": str(mobile_number),
#                 "verificationId": verification_id,
#                 "customerId": settings.MESSAGE_CENTRAL_CUSTOMER_ID,
#                 "code": code,
#             },
#             headers={"authToken": token},
#             timeout=15,
#         )
#         print("VALIDATE RESPONSE:", response.status_code, response.text)
#         data = response.json()
#         return (
#             response.status_code == 200
#             and str(data.get("responseCode")) == "200"
#             and data.get("data", {}).get("verificationStatus") == "VERIFICATION_COMPLETED"
#         )
#     except requests.exceptions.RequestException as e:
#         print("Message Central error:", e)
#         return False