from djongo import models
from django import forms


class Tweet(models.Model):

    objects = models.DjongoManager()


