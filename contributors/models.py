from django.db import models
import uuid
# Create your models here.
# model for frontend purposes
class Contributors(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=50)
    tipe = models.CharField(max_length=50)
    jenis_kelamin = models.IntegerField()
    kewarganegaraan = models.CharField(max_length=50)
    

class Pemain(Contributors):
    pass

class PenulisSkenario(Contributors):
    pass

class Sutradara(Contributors):
    pass