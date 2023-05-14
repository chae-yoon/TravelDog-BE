from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Place, PlaceIMG, Review

User = get_user_model()

class PlaceIMGSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceIMG
        fields = '__all__'

class PlaceListSerializer(serializers.ModelSerializer):
    imageList = PlaceIMGSerializer(many=True, read_only=True)
    review_count = serializers.SerializerMethodField()
    average_star = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ('id', 'pk', 'title', 'address', 'imageList', 'review_count', 'average_star')

    def get_review_count(self, obj):
        return obj.place_reviews.count()
    
    def get_average_star(self, obj):
        reviews = obj.place_reviews.all()
        if reviews:
            total_star = sum(review.star for review in reviews)
            return total_star / len(reviews)
        else:
            return 0.0

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