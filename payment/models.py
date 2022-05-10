from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Demo - add a validator to make sure that the price is >= 0
def valid_price(value):
    if value >= 0:
        return value

    raise ValidationError("Price must be greater than or equal to 0")

class Plan(models.Model):
    'Generated Model'
    name = models.CharField(max_length=256,)
    description = models.TextField()
    price = models.DecimalField(max_digits=30,decimal_places=2,validators=[valid_price])

class Subscription(models.Model):
    'Generated Model'
    app = models.ForeignKey("app.App",on_delete=models.CASCADE,related_name="subscription_app",)
    plan = models.ForeignKey("payment.Plan",on_delete=models.CASCADE,related_name="subscription_plan",)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,)

    # Demo - after we save this subscription, disable all other subscription that exist for this app
    def save(self, *args, **kwargs):
        super(Subscription, self).save(*args, **kwargs)
        other_subs_for_this_app = Subscription.objects.filter(app=self.app).exclude(id=self.id)
        other_subs_for_this_app.update(active=False)
