# api/unit_tests/test_holidays_service.py
from django.test import TestCase
from datetime import datetime, date
from ..services.holidays_service import HolidaysService


class HolidaysServiceTests(TestCase):
    def setUp(self):
        self.service = HolidaysService()

    def test_date_conversion(self):
        """Test la conversion des dates du format ISO au format Django"""
        # Simuler une réponse de l'API
        mock_data = {
            'records': [{
                'fields': {
                    'description': 'Vacances de Noël',
                    'start_date': '2023-12-23T22:00:00+00:00',
                    'end_date': '2024-01-07T22:00:00+00:00',
                    'zones': 'A',
                    'annee_scolaire': '2023-2024'
                }
            }]
        }

        # Formatage des données
        formatted_holidays = self.service._format_holidays(mock_data)
        holiday = formatted_holidays[0]

        # Vérifications
        self.assertIsInstance(holiday['start_date'], date)
        self.assertIsInstance(holiday['end_date'], date)
        self.assertEqual(holiday['start_date'], date(2023, 12, 23))
        self.assertEqual(holiday['end_date'], date(2024, 1, 7))

    def test_api_integration(self):
        """Test l'intégration avec l'API data.gouv.fr"""
        holidays = self.service.get_holidays(zone='A')

        # Vérifications de base
        self.assertTrue(len(holidays) > 0)
        holiday = holidays[0]

        # Vérifier la structure des données
        self.assertIn('description', holiday)
        self.assertIn('start_date', holiday)
        self.assertIn('end_date', holiday)
        self.assertIn('zone', holiday)
        self.assertIn('school_year', holiday)

        # Vérifier les types de données
        self.assertIsInstance(holiday['start_date'], date)
        self.assertIsInstance(holiday['end_date'], date)


    def test_api_error_handling(self):
        """Test la gestion des erreurs de l'API"""
        # Test avec une zone invalide
        holidays = self.service.get_holidays(zone='Z')  # Zone inexistante
        self.assertEqual(len(holidays), 0)  # retourne une liste vide


    def test_school_year_filter(self):
        """Test le filtrage par année scolaire"""
        current_year = datetime.now().year
        school_year = f"{current_year}-{current_year + 1}"
        holidays = self.service.get_holidays(school_year=school_year)
        for holiday in holidays:
            self.assertEqual(holiday['school_year'], school_year)
