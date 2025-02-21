#!/bin/sh

# Définir les variables d'environnement directement dans le script
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=Securepassword123

# Vérifier que les variables d'environnement sont chargées
echo "DJANGO_SUPERUSER_USERNAME: $DJANGO_SUPERUSER_USERNAME"
echo "DJANGO_SUPERUSER_EMAIL: $DJANGO_SUPERUSER_EMAIL"
echo "DJANGO_SUPERUSER_PASSWORD: $DJANGO_SUPERUSER_PASSWORD"

# Attendre que la base de données soit prête
./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up"

# Créer les migrations si elles n'existent pas
if [ ! -d "backend/api/migrations" ]; then
    python manage.py makemigrations api
fi

# Appliquer les migrations
python manage.py migrate

# Vérifier si un superutilisateur existe déjà
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).exists()"; then
    echo "Creating superuser with email: $DJANGO_SUPERUSER_EMAIL, username: $DJANGO_SUPERUSER_USERNAME, and password: $DJANGO_SUPERUSER_PASSWORD"
    python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL --username $DJANGO_SUPERUSER_USERNAME --password $DJANGO_SUPERUSER_PASSWORD --user_type django_admin
else
    echo "Superuser already exists"
fi

# Exécuter le script de configuration des classes par défaut
python manage.py setup_default_classes

# Exécuter le script de configuration des vacances
python manage.py sync_holidays

# Démarrer le serveur
python manage.py runserver 0.0.0.0:8000
