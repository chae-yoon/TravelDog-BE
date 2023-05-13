from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Place, PlaceIMG, Review

class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class PlaceIMGSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceIMG
        fields = '__all__'

class PlaceSerializer(serializers.ModelSerializer):
    imageList = PlaceIMGSerializer(many=True) 

    class Meta:
        model = Place
        fields = '__all__'