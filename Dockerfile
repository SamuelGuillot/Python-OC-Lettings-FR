FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.1.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Installer Poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Copier les fichiers de dépendances
COPY pyproject.toml poetry.lock ./

# Installer les dépendances de production
RUN poetry install --only main --no-root

# Copier le reste du code
COPY . .

# # Rendre build.sh exécutable et l'exécuter pendant le build
# RUN chmod +x build.sh
# RUN ./build.sh

RUN python manage.py collectstatic --noinput

# Utilisateur non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT"]