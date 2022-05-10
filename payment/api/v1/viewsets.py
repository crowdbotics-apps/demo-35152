from rest_framework import authentication
from payment.models import Plan,Subscription
from .serializers import PlanSerializer,SubscriptionSerializer
from rest_framework import viewsets

class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.TokenAuthentication)
    queryset = Plan.objects.all()
    http_method_names = ["get"] # Demo - only let users read plans (Crowdbotics is responsible for other methods)

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.TokenAuthentication)
    http_method_names = ["get", "post"] # Demo - users can read or create new Subscriptions. They cannot be modified so that they can be tracked

    # Demo - custom queryset to make sure we're not returning other user's Subscriptions
    def get_queryset(self):
        return Subscription.objects.filter(app__owner=self.request.user)

