import logging

from django.shortcuts import render

from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    profiles_list = Profile.objects.all()
    logger.info(
        f"Consultation de la liste des profils ({profiles_list.count()})"
    )
    context = {"profiles_list": profiles_list}
    return render(request, "profiles/index.html", context)


def profile(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
        logger.info(f"Consultation du profil : {username}")
    except Profile.DoesNotExist:
        logger.error(f"Profil introuvable : {username}")
        raise
    context = {"profile": profile}
    return render(request, "profiles/profile.html", context)
