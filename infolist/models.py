from django.db import models
import uuid
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
    
    class Meta: 
        abstract = True 

class Series(Tayangan):
    pass 

    
class Film(Tayangan):
    url_video_film = models.CharField(max_length=255)
    release_date_film = models.DateField()
    durasi_film = models.IntegerField()
    
    
class Sutradara(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)