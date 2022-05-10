from django.conf import settings
from django.db import models
class Plan(models.Model):
    'Generated Model'
    name = models.CharField(max_length=256,)
    description = models.TextField()
    price = models.DecimalField(max_digits=30,decimal_places=2,)
class Subscription(models.Model):
    'Generated Model'
    app = models.ForeignKey("app.App",on_delete=models.CASCADE,related_name="subscription_app",)
    plan = models.ForeignKey("payment.Plan",on_delete=models.CASCADE,related_name="subscription_plan",)
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True,)

# Create your models here.
