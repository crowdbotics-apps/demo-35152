
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import AppViewSet
router = DefaultRouter()
router.register('app', AppViewSet, basename='App' ) # Demo - had to add basename here to enable App restriction by owner

urlpatterns = [
    path("", include(router.urls)),
]
