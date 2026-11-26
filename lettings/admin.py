"""Configuration de l'admin pour l'application lettings."""

from django.contrib import admin

from .models import Address, Letting

admin.site.register(Address)
admin.site.register(Letting)
