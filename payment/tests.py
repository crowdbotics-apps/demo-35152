from django.test import TestCase
from payment.models import Plan
from django.core.exceptions import ValidationError

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


