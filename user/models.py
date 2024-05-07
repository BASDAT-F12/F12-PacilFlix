from django.db import models

class Paket(models.Model):
    nama = models.CharField(max_length=50, primary_key=True)
    harga = models.PositiveIntegerField()
    resolusi_layar = models.CharField(max_length=50)

