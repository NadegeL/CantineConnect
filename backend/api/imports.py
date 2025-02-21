# Django imports
from django.db import models  # Import principal de models
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.crypto import get_random_string
from rest_framework.views import APIView

# Third-party imports
from phonenumber_field.modelfields import PhoneNumberField
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (
    viewsets,
    status,
    serializers
)
from rest_framework.decorators import action
from rest_framework.response import Response

# Python standard library
import datetime
import random
import string
import uuid
