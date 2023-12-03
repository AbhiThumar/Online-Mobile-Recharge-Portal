from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid
# Create your models here.

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=17,validators=[phone_regex],unique=True)
    email_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    
class transactions(models.Model):
    sender=models.CharField(max_length=200,null=True)
    receiver=models.CharField(max_length=200,null=True)
    amount=models.IntegerField(null=True)
    time_transtaction=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return repr(self.time_transtaction)
