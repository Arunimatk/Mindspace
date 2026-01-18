# mindspaceapp/models.py

from django.db import models

class UserModel(models.Model):
    name = models.CharField("Full Name", max_length=100)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "myytable"

    def __str__(self):
        return self.name

class JournalEntry(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.name}"

    




  
