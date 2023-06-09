# Reddit-API-Stocks-Scraping
This is a Python Reddit-API scraping repository that allows you to scrape subreddit data and be able to customize the input data using multiple scripts that can scrape ticker lists and subreddits relevant to a certain ticker.
## Important
Since PRAW is rate limited, it cannot process large amounts of data at once.
I tried as much as possible to avoid rate limitation with a cooldown within the ``Submissions_Scraping.py``

I will try to make a repository using Pushshift soon :)

## Features
- Scraping subreddit data using the Python Reddit API Wrapper(PRAW).
- Fairly customizable repository with scripts that can do the following: 
    - scrape ticker lists and relevant subreddits
    - scrapes submissions including any tickers **Beta**
    - scrapes submissions by a given ticker
    - orders the datasets directories by tickers
- Saves data in a CSV file.


## Getting started
### 1. Clone the repository to your local machine.
```
git clone https://github.com/Alex67985/Reddit-API-Stocks-Scraping/
```
### 2. Dependencies
Make sure you install the required libraries
```
pip install -r requirements.txt
```
### 3. Create a Reddit app to obtain credentials. Follow these [instructions](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps).

### 4. Update  ``praw_credentials.json`` from  ``Scripts`` folder with your Reddit app credentials.
```
{
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "password": "your_password",
    "username": "your_username"
}
```
## Input files
### You can choose to use the given subreddits and tickers from the ``Input_Data`` folder or use ``Tickers_Scraper.py`` and ``Subreddit_Scraping.py`` from  ``Scripts`` folder to generate new csv files

## Submissions scraping
###  ``Submissions_Scraping.py`` is exporting by default a dataset with any tickers in the folder  ``Output_Data/Any_Ticker``

You can tweak some scripts in order to make it work the way you want :)




