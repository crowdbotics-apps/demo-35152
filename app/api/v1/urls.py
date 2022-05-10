
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import AppViewSet
router = DefaultRouter()
# Demo - had to add basename for custom get_queryset()
router.register('app', AppViewSet, basename='App' )

urlpatterns = [
    path("", include(router.urls)),
]
