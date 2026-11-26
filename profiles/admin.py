"""Configuration de l'admin pour l'application profiles."""

from django.contrib import admin

from .models import Profile

admin.site.register(Profile)
