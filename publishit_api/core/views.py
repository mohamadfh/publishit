from rest_framework import viewsets, status ,generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Article, Rating
from .serializers import ArticleSerializer, UserRegistrationSerializer , RatingSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import Http404

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class RatingAPIView(APIView):

    def post(self, request, pk):
        """
        Create or update the rating for a specific article.
        """
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404("Article not found.")

        data = {'article': article.id, 'rating': request.data.get('rating')}
        serializer = RatingSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": {
                "username": user.username,
            },
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)