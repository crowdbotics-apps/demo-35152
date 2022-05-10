from rest_framework import serializers
from app.models import App
from payment.api.v1.serializers import SubscriptionSerializer
from payment.models import Subscription, Plan

class AppSerializer(serializers.ModelSerializer):
    # Demo - add a serializer method to return the an App's current subscription
    # SubscriptionSerializer is "lite" enough that this should be fine.
    # If not, we could just return the Subscription's ID from the @property
    # and then fetch the whole thing later.
    current_subscription = SubscriptionSerializer(required=False)

    def create(self, validated_data):
        # Demo - after we create an app, make sure we default it to a Free subscription for starters
        new_app = App.objects.create(**validated_data)
        # This makes an assumption that Plans have already been put in place, and that a free plan exists.
        # It stands to reason that if there are no plans, you shouldn't be able to create an app.
        free_plan = Plan.objects.get(price=0.0)
        Subscription.objects.create(app=new_app, plan=free_plan)
        return new_app

    class Meta:
        model = App
        fields = "__all__"
