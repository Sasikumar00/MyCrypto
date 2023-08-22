from django.db import models
from django.contrib.auth.models import User

class watchlistModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coinName = models.CharField(max_length=20)
    coinImg = models.CharField(max_length=1000)
    watchType = models.CharField(max_length=7)
    watchTarget = models.DecimalField(max_digits=10, decimal_places=2)
    
