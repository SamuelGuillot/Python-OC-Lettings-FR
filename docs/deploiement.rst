Déploiement
===========

Fonctionnement
--------------

Le déploiement est automatisé par GitHub Actions :

1. **Build & Test** : lint + tests sur toutes les branches.
2. **Docker** : build et push de l'image sur Docker Hub (branche ``master`` uniquement).
3. **Deploy** : déclenchement du Deploy Hook Render (branche ``master`` uniquement).

Configuration requise
---------------------

**Secrets GitHub** : ``DOCKERHUB_USERNAME``, ``DOCKERHUB_TOKEN``, ``RENDER_DEPLOY_HOOK_URL``.

**Variables Render** : ``DATABASE_URL``, ``SECRET_KEY``, ``DEBUG=False``, ``SENTRY_DSN``.

Étapes
------

1. Créer une base PostgreSQL sur Render.
2. Créer un Web Service Docker pointant sur le repo.
3. Renseigner les variables d'environnement.
4. Configurer le Deploy Hook et les secrets GitHub.
5. Pousser sur ``master``.