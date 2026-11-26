import logging

from django.shortcuts import render

from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    """Affiche la liste de tous les profils."""
    profiles_list = Profile.objects.all()
    logger.info(
        f"Consultation de la liste des profils ({profiles_list.count()})"
    )
    context = {"profiles_list": profiles_list}
    return render(request, "profiles/index.html", context)


def profile(request, username):
    """Affiche le détail du profil correspondant au username donné."""
    try:
        profile = Profile.objects.get(user__username=username)
        logger.info(f"Consultation du profil : {username}")
    except Profile.DoesNotExist:
        logger.error(f"Profil introuvable : {username}")
        raise
    context = {"profile": profile}
    return render(request, "profiles/profile.html", context)
