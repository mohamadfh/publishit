import math
from celery import shared_task
from django.db.models import Avg, StdDev
from .models import Article, Rating
from datetime import datetime, timedelta


@shared_task
def update_article_ratings():
    articles = Article.objects.all()

    for article in articles:
        new_ratings = Rating.objects.filter(article=article, created_at__gte=get_last_interval_time())

        if new_ratings.exists():
            # Calculate new average and standard deviation for the interval
            new_avg = new_ratings.aggregate(Avg('rating'))['rating__avg']
            new_std = new_ratings.aggregate(StdDev('rating'))['rating__stddev']
            new_count = new_ratings.count()

            previous_avg = article.previous_average_rating
            previous_std = article.previous_std_dev
            previous_count = article.rating_count

            delta_avg = abs(new_avg - previous_avg)
            delta_std = abs(new_std - previous_std)

            k = 2  # sensitivity constant, adjust as needed
            D = 1 / (1 + k * (delta_avg + delta_std))

            w_prev = previous_count
            w_new = new_count * D

            W = w_prev + w_new

            updated_avg = (w_prev * previous_avg + w_new * new_avg) / W

            updated_std_dev = math.sqrt(
                (w_prev * (previous_std ** 2 + (previous_avg - updated_avg) ** 2) +
                 w_new * (new_std ** 2 + (new_avg - updated_avg) ** 2)) / W
            )

            article.average_rating = updated_avg
            article.previous_average_rating = updated_avg
            article.previous_std_dev = updated_std_dev
            article.rating_count = previous_count + new_count
            article.save()

def get_last_interval_time():
    return datetime.now() - timedelta(hours=6)
