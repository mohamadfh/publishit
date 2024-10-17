from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = Rating.objects.filter(article=self)
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return 0

    def rating_count(self):
        return Rating.objects.filter(article=self).count()

class Rating(models.Model):
    article = models.ForeignKey(Article, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.article.title}: {self.rating}"
