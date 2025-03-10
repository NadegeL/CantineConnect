# api/services/holidays_service.py
import requests
from datetime import datetime


class HolidaysService:
    def __init__(self):
        self.base_url = "https://data.education.gouv.fr/api/records/1.0/search/"
        self.dataset = "fr-en-calendrier-scolaire"

    def get_holidays(self, zone='A', school_year=None):
        params = {
            'dataset': self.dataset,
            'q': f'zones:{zone}',
            'sort': 'start_date'
        }
        if school_year:
            params['refine.annee_scolaire'] = school_year

        response = requests.get(self.base_url, params=params)
        return self._format_holidays(response.json())

    def _format_holidays(self, data):
        holidays = []
        for record in data.get('records', []):
            fields = record.get('fields', {})

            start_date = datetime.fromisoformat(
                fields.get('start_date')).date()
            end_date = datetime.fromisoformat(fields.get('end_date')).date()

            holiday = {
                'description': fields.get('description'),
                'start_date': start_date,
                'end_date': end_date,
                'zone': fields.get('zones'),
                'school_year': fields.get('annee_scolaire')
            }
            holidays.append(holiday)
        return holidays
