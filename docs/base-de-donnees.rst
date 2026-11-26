Base de données
===============

Modèles
-------

**Address** (app ``lettings``)
   Adresse d'une location : numéro, rue, ville, état, code postal, pays.

**Letting** (app ``lettings``)
   Location : titre, clé étrangère vers ``Address``.

**Profile** (app ``profiles``)
   Profil utilisateur : clé étrangère vers ``User``, ville favorite.

Relations
---------

- Un ``Letting`` est lié à une ``Address``.
- Un ``Profile`` est lié à un ``User`` Django.