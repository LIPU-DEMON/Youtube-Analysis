from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from DB.models import push
@receiver(pre_delete,sender=User)
def delete(sender,instance,**kwargs):
    push.objects.filter(user_id = instance.id).delete()
