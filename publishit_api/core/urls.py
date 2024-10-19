from django.urls import path
from .views import ArticleViewSet, RatingAPIView, UserRegistrationView
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('articles/', ArticleViewSet.as_view({'get': 'list', 'post': 'create'})),  # List and create articles
    path('articles/<int:pk>/', ArticleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),  # Retrieve, update, delete an article
    path('articles/<int:pk>/rate/', RatingAPIView.as_view()),  # Create or update a rating for an article
    path('register/', UserRegistrationView.as_view()),  # User registration
    path('api-token-auth/', auth_views.obtain_auth_token),

]
