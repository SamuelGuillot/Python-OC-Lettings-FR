set -o errexit # Arrête le script en cas d'erreur

poetry install --only main --no-root

poetry run python manage.py collectstatic --noinput

poetry run python manage.py migrate

set +e
poetry run python manage.py shell -c "from lettings.models import Letting; exit(0 if Letting.objects.exists() else 1)"
TABLE_VIDE=$?
set -e

if [ $TABLE_VIDE -ne 0 ]; then
    echo "Table vide, chargement des fixtures..."
    poetry run python manage.py loaddata fixtures.json
else
    echo "Des données existent déjà, aucun chargement n'est nécessaire."
fi