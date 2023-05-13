from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import PlaceListSerializer, PlaceSerializer, ReviewSerializer
from .models import Place, PlaceIMG, Review
from rest_framework_jwt.settings import api_settings

# Create your views here.
User = get_user_model()

@api_view(['GET'])
def placeList(request):
    if request.method == 'GET':
        places = get_list_or_404(Place)
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def placeDetail(request, place_pk):
    if request.method == 'GET':
        place = get_object_or_404(Place, pk=place_pk)
        serializer = PlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def reviewList(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    token = request.COOKIES.get('token')
    if token:
        payload = jwt_decode_handler(token)
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(place=place, user=user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)