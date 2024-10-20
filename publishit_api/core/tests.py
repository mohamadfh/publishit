from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import Article, Rating
from django.contrib.auth.models import User


class ArticleViewSetTest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")

        # Generate and store token for the user
        self.token = Token.objects.create(user=self.user)

        # Authenticate the user by setting the token in the headers
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create an article for testing
        self.article = Article.objects.create(title="Test Article", text="Test content")

    def test_get_articles(self):
        url = reverse('article-list')
        response = self.client.get(url)

        # Assert that the request is successful and contains articles
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # At least one article

    def test_create_article(self):
        url = reverse('article-list')
        data = {
            "title": "New Test Article",
            "text": "Content of the new article"
        }
        response = self.client.post(url, data, format='json')

        # Assert that the article is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Article.objects.filter(title="New Test Article").exists())


class RatingAPIViewTest(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password")

        # Generate token and authenticate user
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create an article for testing
        self.article = Article.objects.create(title="Test Article", text="Test content")

    def test_create_rating(self):
        url = reverse('article-rating', args=[self.article.id])
        data = {'rating': 4}

        response = self.client.post(url, data, format='json')

        # Assert that the rating was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.filter(article=self.article).count(), 1)
        self.assertEqual(Rating.objects.first().rating, 4)

    def test_update_rating(self):
        # Create an initial rating
        Rating.objects.create(article=self.article, user=self.user, rating=3)

        # Update the rating
        url = reverse('article-rating', args=[self.article.id])
        data = {'rating': 5}
        response = self.client.post(url, data, format='json')

        # Assert that the rating is updated
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.filter(article=self.article).count(), 1)
        self.assertEqual(Rating.objects.first().rating, 5)
