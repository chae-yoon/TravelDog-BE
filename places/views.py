from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import PlaceListSerializer
from .models import Place, PlaceIMG, Review

# Create your views here.
@api_view(['GET'])
def placeList(request):
    if request.method == 'GET':
        places = get_list_or_404(Place)
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)