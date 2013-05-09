from django.db import models

''' Used to select the current app interface '''
class ApSel(models.Model):
    profile = models.ForeignKey("player_mgr.Profile", editable=False)
    location = models.IntegerField(default=0)
    
class Question(models.Model):
    question = models.CharField(max_length=100)
    a = models.CharField(max_length=100)
    b = models.CharField(max_length=100)
    c = models.CharField(max_length=100)
    d = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)