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

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'article', 'rating']

    def validate_rating(self, value):
        """
        Ensure the rating is between 0 and 5.
        """
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

    def create(self, validated_data):
        """
        Create or update a rating.
        """
        article = validated_data.get('article')
        user = self.context['request'].user
        rating_value = validated_data.get('rating')

        rating, created = Rating.objects.update_or_create(
            article=article,
            user=user,
            defaults={'rating': rating_value}
        )

        return rating