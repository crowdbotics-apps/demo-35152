
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import PlanViewSet,SubscriptionViewSet
router = DefaultRouter()
router.register('plan', PlanViewSet )

# Demo - had to add basename for custom get_queryset()
router.register('subscription', SubscriptionViewSet, basename='Subscription' )

urlpatterns = [
    path("", include(router.urls)),
]
