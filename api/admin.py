from django.contrib import admin

from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'swiper', 'swiped')
    list_filter = ('swiper', 'swiped')
