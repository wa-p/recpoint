from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    first_name = CharField(_("First Name"), blank=True, max_length=255)
    last_name = CharField(_("Last Name"), blank=True, max_length=255)
    address = CharField(_("Address"), blank=True, max_length=255)
    phone = CharField(_("Phone Number"),validators=[phone_regex], blank=True, max_length=255)
    licence_number = CharField(_("Licence Number"), blank=True, max_length=20)
    licence_type =  CharField(_("Licence Type"), blank=True, max_length=20)
    licence_picture = models.ImageField( blank=True, null=True, max_length=200)
    actual_picture = models.ImageField( blank=True, null=True, max_length=200)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
