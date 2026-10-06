from django.db import models


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
