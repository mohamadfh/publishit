import time
from locust import HttpUser, task, between

class ArticleUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """Executed when a simulated user starts."""
        print("Starting user session.")

    @task(20)
    def get_articles(self):
        """Fetch articles using a random user token"""
        token = 'be60a940bbf8d62be50ac7910824fd40e84c6ecc'
        headers = {"Authorization": f"Token {token}"}
        self.client.get("api/articles/", headers=headers, name="api/articles/")
        time.sleep(1)

    @task(1)
    def rate_article(self):
        """Rate an article using a random user token"""
        token = 'be60a940bbf8d62be50ac7910824fd40e84c6ecc'
        headers = {"Authorization": f"Token {token}"}
        rating_payload = {
            "rating": 4
        }
        self.client.post("api/articles/1/rate/", json=rating_payload, headers=headers, name="api/articles/1/rate/")
        time.sleep(1)
