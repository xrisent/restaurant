from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]