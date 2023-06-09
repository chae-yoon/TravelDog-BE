from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import PlaceListSerializer, PlaceSerializer, ReviewSerializer, ReviewDetailSerializer
from .models import Place, PlaceIMG, Review
from rest_framework_jwt.settings import api_settings
from rest_framework.pagination import PageNumberPagination

# Create your views here.
User = get_user_model()

@api_view(['GET'])
def placeList(request):
    if request.method == 'GET':
        places = get_list_or_404(Place)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(places, request)
        # serializer = PlaceListSerializer(places, many=True)
        serializer = PlaceListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
        # return Response(serializer.data, status=status.HTTP_200_OK)

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

@api_view(['GET', 'PUT', 'DELETE'])
def reviewDetail(request, place_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data)
    
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    token = request.COOKIES.get('token')
    if token:
        payload = jwt_decode_handler(token)
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        if user.pk == review.user.pk:
            if request.method == 'PUT':
                serializer = ReviewDetailSerializer(review, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
            elif request.method == 'DELETE':
                review.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
                
        return Response({"message": "해당 리뷰의 작성자가 아닙니다."}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reviewLike(request, place_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk) 
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    token = request.COOKIES.get('token')

    if token:
        payload = jwt_decode_handler(token)
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        if review.like.filter(pk=user.pk).exists():
            review.like.remove(user)
            return Response({"message": "좋아요 취소 success"}, status=status.HTTP_200_OK)
        else:
            review.like.add(user)
            return Response({"message": "좋아요 success"}, status=status.HTTP_200_OK)
                
    return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def placeBookmark(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk) 
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    token = request.COOKIES.get('token')

    if token:
        payload = jwt_decode_handler(token)
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        if place.bookmark.filter(pk=user.pk).exists():
            place.bookmark.remove(user)
            return Response({"message": "북마크 취소 success"}, status=status.HTTP_200_OK)
        else:
            place.bookmark.add(user)
            return Response({"message": "북마크 success"}, status=status.HTTP_200_OK)
                
    return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)