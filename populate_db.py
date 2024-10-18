import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor

# Set up base URLs for your API
BASE_URL = "http://localhost:8000/api"
REGISTER_URL = f"{BASE_URL}/register/"
ARTICLES_URL = f"{BASE_URL}/articles/"
RATINGS_URL = f"{BASE_URL}/ratings/"
LOGIN_URL = f"{BASE_URL}/api-token-auth/"

# Number of users and articles
NUM_USERS = 500000
NUM_ARTICLES = 10


# Create 10 articles
def create_articles():
    print("Creating articles...")
    for i in range(1, NUM_ARTICLES + 1):
        article_data = {
            "title": f"Article {i}",
            "text": f"This is the text for article {i}"
        }
        response = requests.post(ARTICLES_URL, json=article_data)
        if response.status_code == 201:
            print(f"Article {i} created.")
        else:
            print(f"Failed to create Article {i}: {response.text}")


# Generate a random username
def generate_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# Register a user
def register_user(username, password="password123"):
    user_data = {
        "username": username,
        "password": password,
    }
    response = requests.post(REGISTER_URL, json=user_data)
    if response.status_code == 201:
        return username
    return None


# Login user and get token
def login_user(username, password="password123"):
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(LOGIN_URL, json=login_data)
    if response.status_code == 200:
        return response.json().get("token")
    return None


# Rate an article
def rate_article(user_token, article_id, rating_value):
    headers = {
        "Authorization": f"Token {user_token}"
    }
    rating_data = {
        "article": article_id,
        "rating": rating_value
    }
    response = requests.post(RATINGS_URL, json=rating_data, headers=headers)
    if response.status_code == 201:
        return f"Rating of {rating_value} for article {article_id} successful."
    return f"Failed to rate article {article_id}: {response.text}"


# Register users, login, and rate articles
def create_users_and_rate_articles(num_users=500000):
    print("Creating users and rating articles...")

    # Create a thread pool to speed up user registration, login, and rating
    with ThreadPoolExecutor(max_workers=100) as executor:
        for i in range(1, num_users + 1):
            username = generate_username()

            # Register the user
            registered_user = register_user(username)
            if registered_user:
                print(f"User {username} created.")

                # Log in the user to get the token
                token = login_user(username)
                if token:
                    # Rate a random article with a random rating between 1 and 5
                    article_id = random.randint(1, NUM_ARTICLES)
                    rating_value = random.randint(1, 5)
                    executor.submit(rate_article, token, article_id, rating_value)
                    print(f"User {username} rated article {article_id} with {rating_value}.")
                else:
                    print(f"Login failed for user {username}.")
            else:
                print(f"Failed to create user {username}.")


# Main function to execute the script
if __name__ == "__main__":
    # Step 1: Create articles
    create_articles()

    # Step 2: Create users, log in, and rate articles
    create_users_and_rate_articles(num_users=NUM_USERS)
