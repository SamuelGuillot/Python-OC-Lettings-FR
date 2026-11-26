## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.12 ou supérieure
- Poetry

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/SamuelGuillot/Python-OC-Lettings-FR.git`

#### Installer les dépendances

- `cd /path/to/Python-OC-Lettings-FR`
- `poetry install`

#### Configurer les variables d'environnement

Créer un fichier `.env` à la racine :

```env
DEBUG=True
SECRET_KEY=dev-only-insecure-key
```

(Laissez `DATABASE_URL` commenté en local : SQLite est utilisé par défaut.)

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `poetry run python manage.py migrate`
- `poetry run python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `poetry run flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `poetry run pytest --cov=. --cov-report=term-missing`

La couverture exclut migrations, fichiers de test, `manage.py`, `settings.py`, `wsgi.py`, `asgi.py`, `apps.py` et `__init__.py` (voir `pyproject.toml`).

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(profiles_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  profiles_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Password123`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Installer Poetry : `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -`
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement

### Fonctionnement (haut niveau)

Le déploiement est entièrement automatisé par **GitHub Actions** en 3 jobs séquencés :

1. **Build & Test** — sur toutes les branches : lint (`flake8`) + tests (`pytest`) avec couverture > 80 %.
2. **Docker** — sur `master` uniquement, si le job 1 réussit : build de l'image et push sur Docker Hub (tags `latest` et hash de commit).
3. **Deploy** — sur `master` uniquement, si le job 2 réussit : déclenche le Deploy Hook Render.

En production, l'application tourne sur **Render** (service Docker) avec une base **PostgreSQL** managée. Les erreurs et logs sont remontés à **Sentry**.

### Configuration requise

**Secrets GitHub** (Settings → Secrets and variables → Actions) :

| Secret | Valeur |
|---|---|
| `DOCKERHUB_USERNAME` | Nom d'utilisateur Docker Hub |
| `DOCKERHUB_TOKEN` | Token d'accès Docker Hub (Read/Write) |
| `RENDER_DEPLOY_HOOK_URL` | URL du Deploy Hook Render |

**Variables d'environnement Render** (Settings → Environment) :

| Variable | Valeur |
|---|---|
| `DATABASE_URL` | Internal Database URL de la base PostgreSQL Render |
| `SECRET_KEY` | Clé secrète Django |
| `DEBUG` | `False` |
| `SENTRY_DSN` | DSN du projet Sentry |
| `SENTRY_ENVIRONMENT` | `production` |
| `PYTHON_VERSION` | `3.12.3` |

### Étapes de déploiement

1. Créer une base **PostgreSQL** sur Render (plan Free), copier l'**Internal Database URL**.
2. Créer un **Web Service** Docker pointant sur le repo (branche `master`, Dockerfile `./Dockerfile`).
3. Renseigner les variables d'environnement Render (tableau ci-dessus).
4. Créer un **Deploy Hook** (Settings → Deploy Hook) et copier l'URL.
5. Configurer les secrets GitHub (tableau ci-dessus).
6. `git push origin master` → le pipeline s'exécute automatiquement.

### Accès admin en production

- URL : `https://oc-lettings-xq70.onrender.com/admin/`
- Identifiants : `admin` / `Password123`

### Limitation du plan Free Render

La base PostgreSQL gratuite **expire après 30 jours**. Pour un usage continu :

- Passer à un plan payant, **ou**
- Recréer une base et recharger les données :
  1. Mettre à jour `DATABASE_URL` dans Render.
  2. Ajouter temporairement `python manage.py loaddata fixtures.json` dans le `CMD` du `Dockerfile`, redéployer, puis retirer la ligne.

Le `Dockerfile` final ne contient **aucune logique de seed automatique** : les données sont chargées une seule fois, et le serveur ne fait qu'appliquer les migrations au démarrage.