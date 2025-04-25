from django.forms import ModelForm
from .models import store
class storeroom(ModelForm):
    class Meta:
        model = store
        fields = ['links']

    
