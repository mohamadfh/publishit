from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Rating

class ArticleSerializer(serializers.ModelSerializer):
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'average_rating', 'rating_count', 'user_rating']

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            rating = Rating.objects.filter(article=obj, user=user).first()
            if rating:
                return rating.rating
        return None

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password']



    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

from django.db.models import Avg, Count

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'article', 'rating']

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

    def create(self, validated_data):
        article = validated_data.get('article')
        user = self.context['request'].user
        rating_value = validated_data.get('rating')

        # Create or update the rating
        rating, created = Rating.objects.update_or_create(
            article=article,
            user=user,
            defaults={'rating': rating_value}
        )

        # Recalculate the article's average rating and rating count
        # self.update_article_rating(article)

        return rating

    def update_article_rating(self, article):
        ratings = Rating.objects.filter(article=article)
        article.average_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        article.rating_count = ratings.aggregate(Count('id'))['id__count']
        article.save()
