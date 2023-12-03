from django.db import models

class OTP(models.Model):
    mobile_number = models.CharField(max_length=20, primary_key=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

def save_otp_to_model(mobile_number, otp):
    # Create or update OTP record in Django model
    otp_object = OTP.objects.get_or_create(mobile_number=mobile_number)
    otp_object.otp = otp
    otp_object.save()
