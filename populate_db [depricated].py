import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # You can use tqdm for progress bars (optional)

# Set up base URLs for your API
BASE_URL = "http://188.121.122.188:8000/api"
REGISTER_URL = f"{BASE_URL}/register/"
ARTICLES_URL = f"{BASE_URL}/articles/"
RATINGS_URL = f"{BASE_URL}/ratings/"
LOGIN_URL = f"{BASE_URL}/api-token-auth/"

# Number of users and articles
NUM_USERS = 50
NUM_ARTICLES = 20
MAX_WORKERS = 10  # Adjust the number of parallel threads
PROGRESS_PRINT_STEP = 10  # Print progress every n steps

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

# Create articles using a token from a registered user
def create_articles(user_token):
    headers = {
        "Authorization": f"Token {user_token}"
    }
    print("Creating articles...")
    for i in range(1, NUM_ARTICLES + 1):
        article_data = {
            "title": f"Article {i}",
            "text": f"This is the text for article {i}"
        }
        response = requests.post(ARTICLES_URL, json=article_data, headers=headers)
        if response.status_code == 201:
            pass  # Article created
        else:
            pass  # Failed to create article

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
        pass  # Rating successful
    return

# Function to register and login a user
def register_and_login_user(progress_counter=None):
    username = generate_username()

    # Register the user
    registered_user = register_user(username)
    if registered_user:
        # Log in the user to get the token
        token = login_user(username)
        if token:
            if progress_counter:
                progress_counter['count'] += 1
                if progress_counter['count'] % PROGRESS_PRINT_STEP == 0:
                    print(f"{progress_counter['count']} users registered and logged in.")
            return token
    return None

# Register users, login, and rate articles
def create_users_and_rate_articles_parallel(num_users=NUM_USERS):
    print(f"Creating {num_users} users in parallel and rating articles...")

    user_tokens = []
    progress_counter = {'count': 0}

    # Step 1: Register users and log them in concurrently
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(register_and_login_user, progress_counter) for _ in range(num_users)]

        # Collect user tokens
        for future in as_completed(futures):
            token = future.result()
            if token:
                user_tokens.append(token)

    print(f"{len(user_tokens)} users registered and logged in successfully.")

    # Step 2: Use the first user's token to create articles
    if user_tokens:
        create_articles(user_tokens[0])

    # Step 3: Use the other users' tokens to rate articles concurrently
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for token in user_tokens:
            for _ in range(4):  # Each user rates 4 articles
                article_id = random.randint(1, NUM_ARTICLES)
                rating_value = random.randint(1, 5)
                executor.submit(rate_article, token, article_id, rating_value)

# Main function to execute the script
if __name__ == "__main__":
    # Step 1: Create users, log in, and rate articles in parallel
    create_users_and_rate_articles_parallel(num_users=NUM_USERS)
