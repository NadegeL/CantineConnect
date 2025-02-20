# app_imports.py
from .models import (
    User,
    Parent,
    Student,
    Administration,
    Address,
    SchoolClass,
    Allergy,
    SchoolZone,
    Holidays
)

from .serializers import (
    UserSerializer,
    ParentSerializer,
    StudentSerializer,
    AdministrationSerializer,
    AddressSerializer,
    SchoolClassSerializer,
    AllergySerializer,
    SchoolZoneSerializer,
    HolidaysSerializer
)
