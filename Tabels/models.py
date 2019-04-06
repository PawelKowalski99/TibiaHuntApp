from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=50)
    level = models.DecimalField(max_digits=5, decimal_places=0)
    vocation = models.CharField(max_length=50)
    server_name = models.CharField(max_length=20)
    guild_name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Servers(models.Model):
    name = models.CharField(max_length=30)
    link = models.URLField(max_length=500)
    players_online = models.DecimalField(max_digits=5, decimal_places=0)
    guild_name = models.CharField(max_length=40)
    def __str__(self):
        return self.name


class NameForm(forms.Form):
    level_req = forms.CharField(label='Your name', max_length=100)

class Post(models.Model):
    post = models.CharField(max_length=500)


