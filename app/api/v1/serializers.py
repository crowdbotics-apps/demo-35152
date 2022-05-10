from rest_framework import serializers
from app.models import App
from payment.api.v1.serializers import SubscriptionSerializer

class AppSerializer(serializers.ModelSerializer):
    # Demo - add a serializer method to return the an App's current subscription
    # SubscriptionSerializer is "lite" enough that this should be fine.
    # If not, we could just return the Subscription's ID from the @property
    # and then fetch the whole thing later.
    current_subscription = SubscriptionSerializer()

    class Meta:
        model = App
        fields = "__all__"
