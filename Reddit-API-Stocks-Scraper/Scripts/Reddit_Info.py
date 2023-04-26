import json
import praw

def reddit_info():
    with open('praw_credentials.json', 'r') as f:
        credentials = json.load(f)
    reddit = praw.Reddit(
        client_id=credentials['client_id'], 
        client_secret=credentials['client_secret'], 
        password=credentials['password'], 
        user_agent="Reddit API Stocks Scraper", 
        username=credentials['username'], 
    )
    return reddit