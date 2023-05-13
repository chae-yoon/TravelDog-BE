from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Place, PlaceIMG, Review

class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'