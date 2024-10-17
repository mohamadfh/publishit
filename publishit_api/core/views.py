from rest_framework import viewsets, status ,generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Article, Rating
from .serializers import ArticleSerializer, UserRegistrationSerializer , RatingSerializer
from django.contrib.auth.models import User

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_serializer_context(self):
        """
        Pass the request context to the serializer to access the current user.
        """
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle the user context without requiring
        it in the request body.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Save the serializer with the current user.
        """
        serializer.save(user=self.request.user)  # Automatically attach the authenticated user

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