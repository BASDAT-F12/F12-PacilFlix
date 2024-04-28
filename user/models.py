from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class Pengguna(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    # id_tayangan = models.ForeignKey('infolist.Tayangan', on_delete=models.CASCADE)
    country = models.CharField(max_length=50, blank=False, null=False)
    USERNAME_FIELD = 'username'

class Paket(models.Model):
    nama = models.CharField(max_length=50, primary_key=True)
    harga = models.PositiveIntegerField()
    resolusi_layar = models.CharField(max_length=50)

