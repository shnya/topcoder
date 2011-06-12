from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProblemType(models.Model):
    level = models.IntegerField()
    division = models.IntegerField()
    class Admin:
        pass

class Problem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    ptypes = models.ManyToManyField(ProblemType)
    class Admin:
        pass
    
class Round(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    problems = models.ManyToManyField('Problem')
    class Admin:
        pass

class History(models.Model):
    user = models.ForeignKey(User)
    round = models.ForeignKey(Round)
    problem = models.ForeignKey(Problem)
    is_practice = models.BooleanField()
    memo = models.TextField()
    code = models.TextField()
    ctime = models.DateTimeField()
    mtime = models.DateTimeField()
    class Admin:
        pass
    
