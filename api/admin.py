from django.contrib import admin

from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('swiper', 'swiped')
    list_filter = ('swiper__email', 'swiped__email')
