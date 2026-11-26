import logging

from django.shortcuts import render

from .models import Letting

logger = logging.getLogger(__name__)


def index(request):
    """Affiche la liste de toutes les locations."""
    lettings_list = Letting.objects.all()
    logger.info(
        f"Consultation de la liste des lettings ({lettings_list.count()})"
    )
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)


def letting(request, letting_id):
    """Affiche le détail d'une location identifiée par son id."""
    try:
        letting = Letting.objects.get(id=letting_id)
        logger.info(f"Consultation du letting id={letting_id}")
    except Letting.DoesNotExist:
        logger.error(f"Letting introuvable : id={letting_id}")
        raise
    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "lettings/letting.html", context)
