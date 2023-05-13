from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Place, PlaceIMG, Review

User = get_user_model()

class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class PlaceIMGSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceIMG
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class AuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username',)

    user = AuthorSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('user', 'star', 'content')
        read_only_fields=('place', )

class ReviewDetailSerializer(serializers.ModelSerializer):
    class AuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username',)

    like = AuthorSerializer(many=True,read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields=('place', 'user')

class PlaceSerializer(serializers.ModelSerializer):
    class AuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username',)

    bookmark = AuthorSerializer(many=True,read_only=True)
    imageList = PlaceIMGSerializer(many=True, read_only=True) 
    place_reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = '__all__'