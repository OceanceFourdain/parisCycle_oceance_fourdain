from django.db import models
from django.utils import timezone

# Create your models here.

class Article(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    titlesArticle = models.CharField(max_length=250)
    descriptionArticle = models.TextField(null=True) #
    urlImageArticle = models.TextField(null=True) # Link the image stock in apps
    createArticle = models.DateTimeField(default=timezone.now)
    updateArticle = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.descriptionArticle