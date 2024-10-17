from django.urls import path

from .views import ArticleViewSet

urlpatterns = [
    path('articles/', ArticleViewSet.as_view({ 'get': 'list' })),
]
