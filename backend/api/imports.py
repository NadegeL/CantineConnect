# Django imports
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin,
                                        AbstractUser
)

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import (
    MinLengthValidator,
    RegexValidator
)
from django.utils.crypto import get_random_string
from django.apps import apps

# DRF imports
from rest_framework import (
    viewsets,
    status,
    serializers,
    generics,
    permissions
)
from rest_framework.decorators import (
    action,
    api_view,
    permission_classes
)
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView

# Third-party imports
from phonenumber_field.modelfields import PhoneNumberField
from drf_yasg.utils import swagger_auto_schema

# Python standard library
import datetime
import random
import string
import uuid
import logging
