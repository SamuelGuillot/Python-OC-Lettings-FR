Interfaces de programmation
===========================

URLs principales
----------------

.. list-table::
   :header-rows: 1

   * - URL
     - Vue
     - Description
   * - ``/``
     - ``oc_lettings_site.views.index``
     - Page d'accueil
   * - ``/lettings/``
     - ``lettings.views.index``
     - Liste des locations
   * - ``/lettings/<id>/``
     - ``lettings.views.letting``
     - Détail d'une location
   * - ``/profiles/``
     - ``profiles.views.index``
     - Liste des profils
   * - ``/profiles/<username>/``
     - ``profiles.views.profile``
     - Détail d'un profil
   * - ``/admin/``
     - (Django admin)
     - Interface d'administration