from django.db import models


class Keyword(models.Model):
    word = models.CharField(max_length=255)
    games_used = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subword(models.Model):
    word = models.CharField(max_length=255)
    games_used = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    keywords = models.ManyToManyField(Keyword, related_name="subwords")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
