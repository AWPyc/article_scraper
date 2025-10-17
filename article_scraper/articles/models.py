from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    html_content = models.TextField(blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    url = models.CharField(max_length=200, blank=False, null=False, unique=True)
    published = models.DateTimeField(blank=False, null=False)