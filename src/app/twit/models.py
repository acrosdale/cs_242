from djongo import models

class Tweet(models.Model):

    objects = models.DjongoManager()


