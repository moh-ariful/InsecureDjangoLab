from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model Posting
class Posting(models.Model):
    judul = models.CharField(max_length=200)
    konten = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images')
    date = models.DateTimeField()
    penulis = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.judul
