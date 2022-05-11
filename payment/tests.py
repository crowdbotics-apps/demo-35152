import json
from django.test import TestCase, Client
from payment.models import Plan, Subscription
from django.core.exceptions import ValidationError
from app.tests import base_app_setup
from app.models import App

client = Client()

# Demo - writing tests
class PlanTest(TestCase):
    def setUp(self):
        self.free_plan = Plan.objects.create(
            name="Free",
            description="Limited access for getting started",
            price=0.0
        )

    def test_plan_model(self):
        self.assertEqual(self.free_plan.name, "Free")
        self.assertEqual(self.free_plan.description, "Limited access for getting started")
        self.assertEqual(self.free_plan.price, 0.0)

    def test_plan_valid_price(self):
        standard_plan = Plan.objects.create(
            name="Standard",
            description="Standard access.",
            price=10.0
        )
        self.assertEqual(standard_plan.price, 10.0)


    def test_plan_free_price(self):
        standard_plan = Plan.objects.create(
            name="Free",
            description="Limited access.",
            price=0.0
        )
        self.assertEqual(standard_plan.price, 0.0)


    def test_plan_invalid_price(self):
        try:
            negative_plan = Plan.objects.create(
                name="Won't work",
                description="Can't have a negative price",
                price=-1.0,
            )
            raise Exception("If this model created, that means test failed")
        except ValidationError as e:
            # We expect a ValidationError to be thrown
            # This is good, the test passed
            pass


class SubscriptionTest(TestCase):
    def setUp(self):
        self.user, _, self.plan1 = base_app_setup()
        self.plan2 = Plan.objects.create(price=10.0, name="Standard", description="Common")
        self.plan3 = Plan.objects.create(price=25, name="Pro", description="Everything we've got")

        self.valid_app_payload = {
            "name": "App",
            "description": "foo",
            "owner": self.user.id
        }

    def active_sub_helper(self, total_subscriptions_count, app):
        """
            Checks that there are the expected total number of subscriptions per an app,
            and there is always exactly 1 active subscription per app.
        """
        all_subscriptions = Subscription.objects.filter(app=app)
        self.assertEqual(all_subscriptions.count(), total_subscriptions_count)
        actives = [sub.active for sub in all_subscriptions]
        # This tests that there is only one active
        self.assertEqual(sum(actives), 1)


    def test_creating_subscription_deactivates_others(self):
        # Create an app, and make sure there is one subscription
        self.assertEqual(Subscription.objects.all().count(), 0)
        client.post(
            "/api/v1/app/",
            data=json.dumps(self.valid_app_payload),
            content_type="application/json"
        )
        app = App.objects.get(name=self.valid_app_payload.get("name"))
        self.active_sub_helper(1, app)

        # keep creating additional subscriptions for the app,
        # and make sure that there is only 1 active subscription for that app
        client.post(
            "/api/v1/subscription/",
            data=json.dumps({
                "app": app.id,
                "plan": self.plan1.id
            }),
            content_type="application/json"
        )
        self.active_sub_helper(2, app)
        client.post(
            "/api/v1/subscription/",
            data=json.dumps({
                "app": app.id,
                "plan": self.plan2.id
            }),
            content_type="application/json"
        )
        self.active_sub_helper(3, app)
