import base64
import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

USER_TYPES = (
    ('ADMIN', 'ADMIN'),
    ('REGULAR', 'REGULAR')
)


class MyUser(AbstractUser):
    user_type = models.CharField(max_length=30, choices=USER_TYPES)
    email = models.EmailField(_('adresse email'), blank=False, unique=True)
    birth_date = models.DateField(verbose_name=_('Date de naissance'), default=timezone.now)
    phone = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    user_token = models.UUIDField(editable=True, default=uuid.uuid4)
    one_factor_auth_enabled = models.BooleanField(default=False)
    one_factor_code = models.CharField(max_length=12)
    nfc = models.CharField(max_length=20, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_birth_date(self):
        pass

    def get_one_factor_code(self):
        return base64.b64decode(bytes(self.one_factor_code[1:], 'utf-8')).decode()

    @classmethod
    def generate_random_etan_password(cls):
        password = cls.objects.make_random_password(length=6)
        return password


AUTH_TYPES = (
    ('NFC', 'NFC'),
    ('PASSWORD', 'PASSWORD')
)


class LoginEntry(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name="login_entries")
    auth_type = models.CharField(choices=AUTH_TYPES, max_length=50)


class RecordConfig(models.Model):
    nb_records=models.IntegerField(default=10)