import uuid
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Article, Rating
import random
from django.db.models import Avg, Count

class Command(BaseCommand):
    help = 'Generate dummy data for Article, Rating, and User models'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Step 1: Create 20 articles
        articles = []
        for i in range(20):
            article = Article.objects.create(
                title=fake.sentence(),
                text=fake.paragraph()
            )
            articles.append(article)
        print(f"20 Articles created.")

        # Step 2: Create 1,000,000 users and 5 ratings per user
        user_batch_size = 10000  # Create users in batches
        total_users = 100000
        ratings_per_user = 5

        for i in range(0, total_users, user_batch_size):
            users = []
            ratings = []

            print(f"Creating users batch {i+1} to {i+user_batch_size}...")
            for j in range(user_batch_size):
                # Use UUID for guaranteed unique usernames
                username = str(uuid.uuid4())
                user = User(username=username, password="password123")
                users.append(user)

            # Bulk create users to save time
            User.objects.bulk_create(users)
            print(f"Batch {i+1}-{i+user_batch_size} users created.")

            # Fetch the users from the database after bulk insert
            user_ids = User.objects.values_list('id', flat=True).order_by('-id')[:user_batch_size]

            print(f"Creating ratings for batch {i+1}-{i+user_batch_size}...")
            for user_id in user_ids:
                selected_articles = random.sample(articles, ratings_per_user)  # Select 5 random articles
                for article in selected_articles:
                    rating_value = random.randint(1, 5)
                    rating = Rating(
                        user_id=user_id,
                        article=article,
                        rating=rating_value
                    )
                    ratings.append(rating)

                    # Update article's average rating and rating count
                    article.rating_count += 1
                    article.average_rating = (
                        (article.average_rating * (article.rating_count - 1) + rating_value)
                        / article.rating_count
                    )
                    article.save()

            # Bulk create ratings to save time
            Rating.objects.bulk_create(ratings)
            print(f"Batch {i+1}-{i+user_batch_size} ratings created.")

        print("Dummy data generation completed.")
