from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from app.models import App
from payment.models import Plan, Subscription
from rest_framework import status
import json
client = Client()

# In a fully-featured service, this setup function would probably get used in a lot of tests
def base_app_setup():
    user = User.objects.create(username="user1")
    app = App.objects.create(name="App 1", description="foo", owner=user)
    plan = Plan.objects.create(price=0.0, name="Free", description="Limited Access")
    return user, app, plan

# Demo - writing tests
class AppTest(TestCase):
    def setUp(self):
        self.user, self.app, self.plan = base_app_setup()

        self.valid_app_payload = {
            "name": "App 2",
            "description": "bar",
            "owner": self.user.id
        }
        self.invalid_app_payload = {
            "name": "App 2",
            "owner": self.user.id
        }

    def test_app_model(self):
        self.assertEqual(self.app.name, "App 1")
        self.assertEqual(self.app.description, "foo")
        self.assertEqual(self.app.owner, self.user)

    def test_post_app(self):
        # make sure there are no subscriptions at first
        all_subscriptions = Subscription.objects.all()
        self.assertEqual(all_subscriptions.count(), 0)
        response = client.post(
            "/api/v1/app/",
            data=json.dumps(self.valid_app_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app2 = App.objects.get(name=self.valid_app_payload.get("name"))

        # now there should be one subscription
        all_subscriptions = Subscription.objects.all()
        self.assertEqual(all_subscriptions.count(), 1)
        subscription = all_subscriptions.first()
        # and it should be tied to the app
        self.assertEqual(app2.current_subscription, subscription)
        self.assertEqual(subscription.app, app2)
        self.assertEqual(subscription.plan, self.plan)

    def test_post_app_invalid(self):
        # if we pass in a bad payload, it should 400
        response = client.post(
            "/api/v1/app/",
            data=json.dumps(self.invalid_app_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
