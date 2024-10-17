from rest_framework import permissions, viewsets
from .serializers import ArticleSerializer
from .models import Article

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]
