#!/bin/sh

# Charger les variables d'environnement
export $(grep -v '^#' .env | xargs)

# Attendre que la base de données soit prête
./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up"

# Créer les migrations si elles n'existent pas
if [ ! -d "backend/api/migrations" ]; then
    python manage.py makemigrations api
fi

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur si aucun n'existe
echo "from django.contrib.auth import get_user_model; \
import os; \
from dotenv import load_dotenv; \
load_dotenv(); \
User = get_user_model(); \
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin'); \
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'); \
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'Securepassword123'); \
User.objects.create_superuser(username, email, password) \
if not User.objects.filter(is_superuser=True).exists() else print('Superuser already exists')" | python manage.py shell


# Exécuter le script de configuration des classes par défaut
python manage.py setup_default_classes

# Exécuter le script de configuration des vacances
python manage.py sync_holidays

# Démarrer le serveur
python manage.py runserver 0.0.0.0:8000
