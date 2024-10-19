# Publish It

This app is designed to manage articles and allow users to rate them. Users can create articles with a title and text, and other users can give ratings (between 1 and 5) 
to these articles. The app stores the users, articles, and ratings in a database, and for each article, it calculates the average rating and the total number of ratings.

## Regarding Scalibility

### Scalability and Load Testing

To test the scalability of my application, I needed to insert a large amount of data, 
specifically millions of users and ratings. I created 1,000,000 users and had each user rate 5 articles, with a total of 20 articles. 
This approach allowed me to simulate a real-world scenario where many users interact with the system, helping me to evaluate how the application performs under load.

### Baseline Naive Solution

To set a baseline for comparison, I implemented a simple and inefficient solution to check how well the system could handle the load in its most basic form. This naive approach performed a **count query for ratings** each time an article was displayed:

- **Naive Query**: Every time an article was shown, I performed a query like this: `Rating.objects.filter(article=article).count()`. This query counts the number of ratings for the article on each request.
  
- **Performance Impact**: Although this approach is simple, it can be very slow when there are millions of ratings, as the database has to count rows repeatedly, especially if the table is large and not indexed properly.

### Why the Naive Approach?

I used this naive approach as a baseline for comparison with more optimized solutions. The purpose was to understand how bad performance could be if no optimizations were applied, and then measure the improvements from more efficient approaches, such as caching counts or using database-level optimizations (e.g., indexed columns, materialized views).

By comparing the baseline performance with more optimal solutions, I could better understand the impact of improvements and how much faster the system could become when handling a large number of users and ratings.
### results

After generating 100000 users and 500000 ratings in the database, I used locust to perform load test on my api. Here is the result for 200 active users making requests:

![result 200 local](https://github.com/mohamadfh/publishit/blob/main/reports/200%20local.png?raw=true)

Here is the result for 500 active users making requests:

![result 500 local](https://github.com/mohamadfh/publishit/blob/main/reports/500%20local.png?raw=true)

![result 500 local](https://github.com/mohamadfh/publishit/blob/main/reports/500%20local%20chart.png?raw=true)

