from django.db import models
import uuid
from user.models import Pengguna
# Create your models here.
# model for frontend purposes
class Tayangan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=100)
    sinopsis = models.CharField(max_length=255)
    asal_negara = models.CharField(max_length=50)
    sinopsis_trailer = models.CharField(max_length=255)
    url_video_trailer = models.CharField(max_length=255)
    release_date_trailer = models.DateField()
    sutradara = models.ForeignKey('Sutradara', on_delete=models.CASCADE)
    

class Series(Tayangan):
    pass 

class Episode(models.Model):
    id_series = models.ForeignKey(Series, on_delete=models.CASCADE)
    sub_judul = models.CharField(max_length=100)
    sinopsis = models.CharField(max_length=255)
    durasi = models.IntegerField(default=0 , null=False)
    url_video = models.CharField(max_length=255, null= False)
    release_date = models.DateField()
   
    class Meta:
       unique_together = ('id_series', 'sub_judul')   
    
class Film(Tayangan):
    url_video_film = models.CharField(max_length=255)
    release_date_film = models.DateField()
    durasi_film = models.IntegerField()
    
class Contributors(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=50, default='Anonim')
    JENIS_KELAMIN_CHOICE = ((0, 'Laki-laki'), (1, 'Perempuan'))
    jenis_kelamin = models.IntegerField(choices=JENIS_KELAMIN_CHOICE, default=0, null=False)
    kewarganegaraan = models.CharField(max_length=50, default='Indonesia')
    
    class Meta:
        abstract = True
    
class Sutradara(Contributors):
    pass

class Pemain(Contributors):
    pass

class Penulis(Contributors):
    pass