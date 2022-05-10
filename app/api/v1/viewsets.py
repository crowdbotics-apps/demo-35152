from rest_framework import authentication
from app.models import App
from .serializers import AppSerializer
from rest_framework import viewsets

class AppViewSet(viewsets.ModelViewSet):
    serializer_class = AppSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.TokenAuthentication)

    # Demo - custom queryset to make sure we're not returning other user's apps
    def get_queryset(self):
        return App.objects.filter(owner=self.request.user)
