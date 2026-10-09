from django.db import models


#admin user role model
class UserRole(models.Model):

    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        db_index=True
    )

    is_admin = models.BooleanField(default=False)

    is_driver = models.BooleanField(default=False)

    is_truckowner = models.BooleanField(default=False)

    is_manufacturer = models.BooleanField(default=False)

    is_transport_vendor = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.mobile_number

    class Meta:
        db_table = "user_roles"



class OTPVerification(models.Model):

    CHANNEL_CHOICES = (
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
    )

    mobile_number = models.CharField(
        max_length=15,
        db_index=True
    )

    otp = models.CharField(max_length=4)

    channel = models.CharField(
        max_length=10,
        choices=CHANNEL_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    attempt_count = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        indexes = [
            models.Index(
                fields=['mobile_number', 'created_at']
            ),
        ]

    def __str__(self):
        return f"{self.mobile_number} - {self.channel}"




# Company Model Details
from django.db import models
class Company(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ("GST", "GST"),
        ("CIN", "CIN"),
        ("OTHER_LICENSE", "Other License"),
    ]

    company_id = models.AutoField(primary_key=True)
    
    company_uniqueid = models.CharField(
        max_length=50,
        unique=True,
        default=0
    )

    company_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    company_person_number = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES
    )

    document = models.FileField(
        upload_to="company_documents/",
        null=True,
        blank=True
    )

    other_document = models.FileField(
        upload_to="company_documents/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "companies"
        ordering = ["-created_at"]



# DriverRegistration
from django.db import models
from django.conf import settings

class DriverRegistration(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    DL_TYPE_CHOICES = (
        ("LMV", "LMV"),
        ("HMV", "HMV"),
        ("LMV_HMV", "LMV + HMV"),
        ("TRANSPORT", "Transport"),
        ("OTHER", "Other"),
    )

    COMPANY_TYPE_CHOICES = (
        ("ivyis", "IVYIS"),
        ("other", "Other Company"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    # =========================
    # USER
    # =========================

    # user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name="driver_registration"
    # )

    # =========================
    # COMPANY
    # =========================

    company_type = models.CharField(
        max_length=10,
        choices=COMPANY_TYPE_CHOICES,
        default="ivyis"
    )

    company = models.ForeignKey(
        "Company",
        on_delete=models.PROTECT,
        related_name="drivers",
        null=True,
        blank=True
    )

    # =========================
    # PERSONAL DETAILS
    # =========================

    name = models.CharField(
        max_length=150
    )

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    mobile_number = models.CharField(
        max_length=15
    )

    # =========================
    # AADHAAR DETAILS
    # =========================

    aadhaar_number = models.CharField(
        max_length=12
    )

    # =========================
    # DRIVING LICENCE DETAILS
    # =========================

    driving_licence_number = models.CharField(
        max_length=30,
        unique=True
    )

    dl_type = models.CharField(
        max_length=20,
        choices=DL_TYPE_CHOICES
    )

    dl_issued_date = models.DateField()

    dl_expired_date = models.DateField()

    # =========================
    # ADDRESS
    # =========================

    permanent_address = models.TextField()

    current_address = models.TextField()

    # =========================
    # DOCUMENTS
    # =========================

    # PDF
    medical_certificate = models.FileField(
        upload_to="drivers/medical_certificates/"
    )

    # PDF
    police_verification_certificate = models.FileField(
        upload_to="drivers/police_verification/"
    )

    # Driver Photo
    photo = models.ImageField(
        upload_to="drivers/photos/"
    )

    # Aadhaar Front & Back
    aadhaar_front = models.ImageField(
        upload_to="drivers/aadhaar/"
    )

    aadhaar_back = models.ImageField(
        upload_to="drivers/aadhaar/"
    )

    # Driving Licence Front & Back
    dl_front = models.ImageField(
        upload_to="drivers/driving_license/"
    )

    dl_back = models.ImageField(
        upload_to="drivers/driving_license/"
    )

    # =========================
    # ADMIN REVIEW
    # =========================

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    rejection_reason = models.TextField(
        null=True,
        blank=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} - {self.driving_licence_number}"

    class Meta:
        db_table = "driver_registrations"
        ordering = ["-created_at"]