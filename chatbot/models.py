from django.db import models
from django.db import models

# Create your models here.
class Mood(models.Model):
    user = models.CharField(max_length=100, default="anonymous")
    mood = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.mood} at {self.timestamp}"
