from django.urls import path
from .views import ArticleViewSet, RatingAPIView, UserRegistrationView
from rest_framework.authtoken import views as auth_views

# Assuming you have the following URL names in your project:
urlpatterns = [
    path('articles/', ArticleViewSet.as_view({'get': 'list', 'post': 'create'}), name='article-list'),
    path('articles/<int:pk>/', ArticleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='article-detail'),
    path('articles/<int:pk>/rate/', RatingAPIView.as_view(), name='article-rating'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('api-token-auth/', auth_views.obtain_auth_token),
]
