from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class store(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    links = models.URLField()
    Time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-Time']
    
    def __str__(self):
        return f"{self.user} - {self.links}"

