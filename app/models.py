from django.conf import settings
from django.db import models
class App(models.Model):
    'Generated Model'
    name = models.CharField(max_length=256,)
    description = models.TextField()
    owner = models.ForeignKey("users.User",on_delete=models.CASCADE,related_name="app_owner",)

    # Demo - easier name field
    def __str__(self):
        return self.name
# Create your models here.
