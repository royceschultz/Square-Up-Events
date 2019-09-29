from django.contrib import admin

from .models import Event

@admin.register(Event)
class eventsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
