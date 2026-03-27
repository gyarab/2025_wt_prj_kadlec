from django.contrib import admin
from .models import Uzivatel, Auto, Rezervace

@admin.register(Uzivatel)
class UzivatelAdmin(admin.ModelAdmin):
    list_display = ('id', 'jmeno', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('jmeno', 'email')

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'znacka_a_model', 'spz', 'rok_vyroby', 'stav_tachometru', 'prevodovka', 'pocet_mist')
    list_filter = ('rok_vyroby', 'prevodovka', 'pocet_mist')
    search_fields = ('znacka_a_model', 'spz')

@admin.register(Rezervace)
class RezervaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'uzivatel', 'auto', 'datum_vyzvednuti', 'misto_vraceni', 'typ_pojisteni', 'stav')
    list_filter = ('stav', 'typ_pojisteni', 'datum_vyzvednuti')
    search_fields = ('uzivatel__jmeno', 'auto__spz', 'misto_vraceni')
