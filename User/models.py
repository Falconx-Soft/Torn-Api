from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class accountsCheck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    crated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class apiInfo(models.Model):
    apiKey = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # crated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class record(models.Model):
    UserId = models.CharField(max_length=100 ,null=True)
    Faction = models.CharField(max_length=100 ,null=True)
    TotalStats = models.IntegerField(null=True)
    Str = models.CharField(max_length=100,null=True)
    Def = models.CharField(max_length=100,null=True)
    Spd = models.CharField(max_length=100,null=True)
    Dex = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.UserId



