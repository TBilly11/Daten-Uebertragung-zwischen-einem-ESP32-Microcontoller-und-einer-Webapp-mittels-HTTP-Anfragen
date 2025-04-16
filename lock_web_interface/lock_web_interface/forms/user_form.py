from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _
import logging
import base64

from lock_web_interface.models import MyUser

logger = logging.getLogger(__name__)

USER_TYPE_CHOICES = (
    ('ADMIN', 'ADMIN'),
    ('REGULAR_USER', 'REGULAR_USER')
)


class BaseUserForm(forms.Form):
    first_name = forms.CharField(required=True, label=_('Prénom'), widget=forms.TextInput(
        attrs={"class": "form-control input-lg", "placeholder": "Baptiste"}))
    last_name = forms.CharField(required=True, label=_('Nom'), widget=forms.TextInput(
        attrs={"class": "form-control input-lg", "placeholder": "Delrue"}))
    email = forms.EmailField(required=True, label=_('Email'), widget=forms.EmailInput(
        attrs={"class": "form-control input-lg", "placeholder": "azerty@gmail.com"}))
    password1 = forms.CharField(required=True, label=_("Mot de passe"), min_length=8,
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control input-lg", "placeholder": "Mot de passe"}))
    password2 = forms.CharField(required=True, label=_("Confirmer le mot de passe"), min_length=8,
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control input-lg", "placeholder": "Confirmer"}))


class AdminForm(BaseUserForm):

    def clean_password1(self):
        password1 = self.data.get('password1', None)
        password2 = self.data.get('password2', None)

        if password1:
            if password1 != password2:
                self.add_error('password2', _('Les mots de passe sont différents'))
            else:
                try:
                    validate_password(password1)
                except ValidationError as val_errors:
                    self.add_error('password1', val_errors)

        else:
            self.add_error('password1', _('Ce champ est requis'))

        return password1

    def save(self):
        try:
            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            user_type = "ADMIN"
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password1')

            user = MyUser.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                user_type=user_type,
                password=password,
                is_active=False
            )
            return user
        except Exception as e:
            logger.error(e)
            raise


class UserForm(BaseUserForm):

    def __init__(self, **kwargs):
        self.user_id = kwargs.pop("user_id")
        super().__init__(**kwargs)
        self.fields['user_id'] = forms.CharField(required=False, widget=forms.HiddenInput(), label="user id",
                                                 initial=self.user_id)
        self.fields.pop('password1')
        self.fields.pop('password2')

    one_factor_code = forms.CharField(required=True, label=_('Code'), widget=forms.TextInput(
        attrs={"class": "form-control input-lg", "placeholder": "code d'authentification à 1 facteur"}))
    username = forms.CharField(required=True, label=_('Username'), widget=forms.TextInput(
        attrs={"class": "form-control input-lg", "placeholder": "Username"}))
    nfc = forms.CharField(required=True, label=_('Code NFC'), widget=forms.TextInput(
        attrs={"class": "form-control input-lg", "placeholder": "code NFC"}))

    def clean(self):
        nfc = self.cleaned_data.get('nfc')
        try:
            MyUser.objects.get(nfc=nfc)
        except MultipleObjectsReturned:
            self.add_error('nfc', "A user with this code already exist")
        except MyUser.DoesNotExist:                                              #ici
            pass
    def save(self):
        try:
            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            username = self.cleaned_data.get('username')
            user_type = "REGULAR"
            email = self.cleaned_data.get('email')
            password = "azerty123"
            one_factor_code = self.cleaned_data.get('one_factor_code')
            nfc = self.cleaned_data.get('nfc')
            if self.user_id:
                user = MyUser.objects.get(id=self.user_id)
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.password = password
                user.one_factor_code = base64.b64encode(bytes(one_factor_code, 'utf-8'))
                user.nfc = nfc
                user.save()
            else:
                user = MyUser.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    user_type=user_type,
                    password=password,
                    one_factor_code=base64.b64encode(bytes(one_factor_code, 'utf-8')),
                    nfc=nfc,
                    is_active=False
                )
            return user
        except Exception as e:
            logger.error(e)
            raise
