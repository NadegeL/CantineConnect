from django.test import TestCase
from ..factories import HolidaysFactory, SchoolZoneFactory
from datetime import date, timedelta
from ..models import Holidays, SchoolZone


class HolidaysTests(TestCase):
    def setUp(self):
        self.zone = SchoolZoneFactory()
        self.today = date.today()
        self.holiday = HolidaysFactory(
            zone=self.zone,
            start_date=self.today,
            end_date=self.today + timedelta(days=14)
        )

    def test_holiday_creation(self):
        """Test la création des vacances"""
        self.assertEqual(self.holiday.zone, self.zone)
        self.assertEqual(self.holiday.start_date, self.today)

    def test_holiday_duration(self):
        """Test la durée des vacances"""
        duration = (self.holiday.end_date - self.holiday.start_date).days
        self.assertEqual(duration, 14)

    def test_current_holidays(self):
        """Test les vacances actuelles"""
        current = Holidays.objects.filter(
            start_date__lte=self.today,
            end_date__gte=self.today
        )
        self.assertTrue(current.exists())
