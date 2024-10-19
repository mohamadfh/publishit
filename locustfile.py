import time
from locust import HttpUser, task, between
from random import choice

class ArticleUser(HttpUser):
    wait_time = between(1, 5)



    def on_start(self):
        """Executed when a simulated user starts."""
        print("Starting user session.")

    @task(20)
    def get_articles(self):
        """Fetch articles using a random user token"""
        token = 'a9a7c094043b64d4d604a693e95fbfa68b64ac10'
        headers = {"Authorization": f"Token {token}"}
        self.client.get("/api/articles/", headers=headers, name="/api/articles/")
        time.sleep(1)

    @task(1)
    def rate_article(self):
        """Rate an article using a random user token"""
        token = 'a9a7c094043b64d4d604a693e95fbfa68b64ac10'
        headers = {"Authorization": f"Token {token}"}
        rating_payload = {
            "article": 1,  # Adjust to actual article ID
            "rating": 4
        }
        self.client.post("/api/ratings/", json=rating_payload, headers=headers, name="/api/ratings/")
        time.sleep(1)
