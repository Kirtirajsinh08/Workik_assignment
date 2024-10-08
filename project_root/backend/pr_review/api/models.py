from django.db import models

# Create your models here.
class GithubUser(models.Model):
    github_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)

class Repository(models.Model):
    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(GithubUser, on_delete=models.CASCADE)
    webhook_id = models.IntegerField(null=True, blank=True)