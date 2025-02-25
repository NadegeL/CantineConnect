from django.core.management.base import BaseCommand
from ...models import SchoolZone, Holidays
from ...services.holidays_service import HolidaysService
from datetime import datetime


class Command(BaseCommand):
    help = 'Synchronise les vacances scolaires depuis data.gouv.fr'

    def handle(self, *args, **kwargs):
        service = HolidaysService()

        for zone_choice in SchoolZone.ZONE_CHOICES:
            zone_code = zone_choice[0]
            zone, created = SchoolZone.objects.get_or_create(name=zone_code)

            holidays = service.get_holidays(zone=zone_code)
            for holiday_data in holidays:
                Holidays.objects.update_or_create(
                    zone=zone,
                    start_date=holiday_data['start_date'],
                    end_date=holiday_data['end_date'],
                    defaults={
                        'description': holiday_data['description'],
                        'school_year': holiday_data['school_year']
                    }
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Zone {zone_code} synchronized successfully')
            )
