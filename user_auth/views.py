from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from restaurant.models import Reservation
from restaurant.serializers import ReservationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Person
from .serializers import PersonSerializer


from .models import *
from .serializers import *

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = serializer.save()


class CurrentUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
        }

        try:
            person = Person.objects.get(user=request.user)
            person_data = PersonSerializer(person).data
        except Person.DoesNotExist:
            person_data = None

        reserved_tables_data = None 

        if person_data is not None:
            reserved_tables = Reservation.objects.filter(reserved_by=person)
            reserved_tables_data = ReservationSerializer(reserved_tables, many=True).data

        response_data = {
            'user_data': user_data,
            'person_data': person_data,
            'reserved_tables': reserved_tables_data,
        }

        return Response(response_data)


class UploadPhotoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            person = Person.objects.get(pk=pk, user=request.user)
        except Person.DoesNotExist:
            return Response({"detail": "Person not found."}, status=status.HTTP_404_NOT_FOUND)

        if 'photo' not in request.FILES:
            return Response({"detail": "No photo provided."}, status=status.HTTP_400_BAD_REQUEST)

        person.photo = request.FILES['photo']
        person.save()
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    