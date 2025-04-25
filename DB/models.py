from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class push(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=500)
    Likes = models.IntegerField()
    views = models.BigIntegerField()
    subs = models.BigIntegerField()
    comments = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    class Meta:
        app_label = 'DB'
        