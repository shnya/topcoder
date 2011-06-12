from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Round(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class Problem(models.Model):
    problemid = models.IntegerField()
    name = models.CharField(max_length=100)
    level = models.IntegerField(db_index=True)
    division = models.IntegerField(db_index=True)
    round = models.ForeignKey(Round)

class History(models.Model):
    user = models.ForeignKey(User)
    round = models.ForeignKey(Round)
    problem = models.ForeignKey(Problem)
    is_practice = models.BooleanField()
    memo = models.TextField()
    code = models.TextField()
    ctime = models.DateTimeField()
    mtime = models.DateTimeField()
    
