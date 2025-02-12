from django.core.management.base import BaseCommand
from api.models import SchoolClass


class Command(BaseCommand):
    help = 'Setup default school classes'

    def handle(self, *args, **kwargs):
        default_classes = [
            'Petite Section', 'Moyenne Section', 'Grande Section',
            'CP', 'CE1', 'CE2', 'CM1', 'CM2',
            '6ème', '5ème', '4ème', '3ème',
            '2nde', '1ère', 'Terminale'
        ]

        for name in default_classes:
            if not SchoolClass.objects.filter(name=name).exists():
                SchoolClass.objects.create(name=name)

        self.stdout.write(self.style.SUCCESS(
            'Default school classes have been set up successfully.'))
