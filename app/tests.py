from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from users.models import User
from app.models import App
from payment.models import Plan
from rest_framework import status
import json
client = Client()


# Demo - writing tests
class AppTest(TestCase):
    def setUp(self):
        self.user =  User.objects.create(username="user1")
        self.app = App.objects.create(name="App 1", description="foo", owner=self.user)
        self.free_plan = Plan.objects.create(price=0.0, name="Free", description="Limited Access")

        self.valid_payload = {
            "name": "App 2",
            "description": "bar",
            "owner": self.user.id
        }
        self.invalid_payload = {
            "name": "App 2",
            "owner": self.user.id
        }

    def test_app_model(self):
        self.assertEqual(self.app.description, "foo")
        self.assertEqual(self.app.owner, self.user)

    def test_post_app(self):
        response = client.post(
            "/api/v1/app/",
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app2 = App.objects.get(name=self.valid_payload.get("name"))
        self.assertEqual(app2.current_subscription.plan, self.free_plan)

    def test_post_app_invalid(self):
        response = client.post(
            "/api/v1/app/",
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
