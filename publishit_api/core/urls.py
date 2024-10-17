from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, RatingViewSet, UserRegistrationView
from rest_framework.authtoken import views as auth_views

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),

    path('api-token-auth/', auth_views.obtain_auth_token),
]
