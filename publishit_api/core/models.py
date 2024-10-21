from django.db import models
from django.contrib.auth.models import User



from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    average_rating = models.FloatField(default=0.0)  # Store the average rating
    rating_count = models.IntegerField(default=0)    # Store the number of ratings
    previous_average_rating = models.FloatField(default=0.0)  # Store previous average
    previous_std_dev = models.FloatField(default=0.0)  # Store previous standard deviation

    def __str__(self):
        return self.title

class Rating(models.Model):
    article = models.ForeignKey(Article, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the rating was created

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.article.title}: {self.rating}"
