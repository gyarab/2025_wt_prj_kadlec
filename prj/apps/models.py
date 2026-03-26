from django.db import models

class Uzivatel(models.Model):
    jmeno = models.CharField(max_length=150, verbose_name="Jméno")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    heslo = models.CharField(max_length=128, verbose_name="Heslo")
    role = models.CharField(max_length=50, verbose_name="Role")

    def __str__(self):
        return self.jmeno

    class Meta:
        verbose_name = "Uživatel"
        verbose_name_plural = "Uživatelé"


class Auto(models.Model):
    znacka_a_model = models.CharField(max_length=100, verbose_name="Značka a model")
    spz = models.CharField(max_length=20, unique=True, verbose_name="SPZ")
    rok_vyroby = models.IntegerField(verbose_name="Rok výroby")
    stav_tachometru = models.IntegerField(verbose_name="Stav tachometru")
    prevodovka = models.CharField(max_length=50, verbose_name="Převodovka")
    pocet_mist = models.IntegerField(verbose_name="Počet míst")

    def __str__(self):
        return f"{self.znacka_a_model} ({self.spz})"

    class Meta:
        verbose_name = "Auto"
        verbose_name_plural = "Auta"


class Rezervace(models.Model):
    uzivatel = models.ForeignKey(Uzivatel, on_delete=models.CASCADE, verbose_name="Uživatel")
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, verbose_name="Auto")
    
    datum_vyzvednuti = models.DateField(verbose_name="Datum vyzvednutí")
    misto_vraceni = models.CharField(max_length=150, verbose_name="Místo vrácení")
    typ_pojisteni = models.CharField(max_length=100, verbose_name="Typ pojištění")
    stav = models.CharField(max_length=50, verbose_name="Stav")

    def __str__(self):
        return f"Rezervace #{self.id} | {self.uzivatel.jmeno} -> {self.auto.znacka_a_model}"

    class Meta:
        verbose_name = "Rezervace"
        verbose_name_plural = "Rezervace"
