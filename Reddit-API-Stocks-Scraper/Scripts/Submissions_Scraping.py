import re
from datetime import datetime
import pandas as pd
from emoji import demojize
import time
from tqdm import tqdm
import Reddit_Info as rd
import os


def get_tickers():
    directory = os.path.join('..', 'Input_Data', 'Tickers')
    filename = 'nasdaq_tickers' #You can specify a ticker csv file here
    filepath = os.path.join(directory, filename)
    tickers = pd.read_csv(f'{filepath}.csv')  
    known_tickers = set(tickers['ticker'])
    return known_tickers


def subreddits(n: int=10): #Takes the top 10 subreddits by default due to rate limit


    subreddits = [] #You can add your own subreddits here without using any subreddit csv file


    directory = os.path.join('..', 'Input_Data', 'Subreddits')
    filename = '_subreddits_2023-04-26_16-54-21' #You can specify a subreddit dataset here
    filepath = os.path.join(directory, filename)
    subreddit_list = pd.read_csv(f'{filepath}.csv') 
    subreddit_list['Subreddit'] = subreddit_list['Subreddit'].str.lower()
    top_n_subreddits = subreddit_list.sort_values('Members', ascending=False)['Subreddit'].unique()[:n]
    return subreddits if subreddits else list(top_n_subreddits)



def generate_submissions_any_ticker(limiter: int = 200, subno: int = 10): 
    sleep_time = 300 if subno >= 21 or limiter >= 25000 else 0 #Applying cooldown due to rate limit of the Reddit API
    count = 0
    reddit = rd.reddit_info()
    ticker_list = get_tickers()
    subreddit_names = subreddits(subno)
    non_tickers = ['US', 'UK', 'TOP', 'API', 'FREE'] #this can be modified
    ticker_pattern = r'\b([A-Z]{2,5}|\$\w+)\b' 
    for subreddit_name in tqdm(subreddit_names, total=subno):
            subreddit = reddit.subreddit(subreddit_name) 
            titles_seen = set()
            
            for submission in subreddit.new(limit=limiter):

                title_no_emoji = demojize(submission.title)
                title_no_emoji = re.sub(r':[a-z_]+:', '', title_no_emoji)  
                tickers = re.findall(ticker_pattern, title_no_emoji) 
                tickers = [t for t in tickers if t not in non_tickers and t in ticker_list]
                for ticker in tickers:
                    if len(tickers) > 0 and submission.title not in titles_seen:
                            titles_seen.add(submission.title)    
                            yield [
                                submission.author,
                                ticker,
                                title_no_emoji,
                                datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                                submission.score,
                                submission.upvote_ratio,
                                subreddit_name
                                ]
            
            count+=1
            if count >= 10 and sleep_time > 0:
                print(" Cooldown for every 10 subreddits")
                time.sleep(sleep_time)
                count = 0 


def generate_submissions_with_ticker(ticker_name: str, limiter: int = 200, subno: int = 10):
    sleep_time = 300 if subno >= 21 or limiter >= 25000 else 0
    count = 0
    reddit = rd.reddit_info()
    ticker = ticker_name
    subreddit_names = subreddits(subno)
    for subreddit_name in tqdm(subreddit_names, total=subno):
            subreddit = reddit.subreddit(subreddit_name) 
            titles_seen = set()
            for submission in tqdm(subreddit.new(limit=limiter), total=limiter, leave=False):
                title_no_emoji = demojize(submission.title)
                title_no_emoji = re.sub(r':[a-z_]+:', '', title_no_emoji)  
                tickers = re.findall(ticker, title_no_emoji) 
                if len(tickers) > 0 and submission.title not in titles_seen:
                            titles_seen.add(submission.title)    
                            yield [
                                submission.author,
                                ticker,
                                title_no_emoji,
                                datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                                submission.score,
                                submission.upvote_ratio,
                                subreddit_name
                                ]
            count+=1
            if count >= 10 and sleep_time > 0:
                print(" Cooldown for every 10 subreddits")
                time.sleep(sleep_time)
                count = 0 





def export_data_any_ticker(max_submisisons=200, subno=10):
    df = pd.DataFrame(generate_submissions_any_ticker(max_submisisons, subno), columns=['User', 'Ticker', 'Text', "Timestamp", "Upvotes", "Ratio", "Subreddit"])
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    directory = os.path.join('..', 'Output_Data', 'Any_Ticker')
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f'reddit_dataset_{timestamp}'
    filepath = os.path.join(directory, filename)
    df.to_csv(f'{filepath}.csv', index=False)
    print(f'{filename} exported to {filepath}')


def export_data_with_ticker(ticker, max_submissions=200, subno=10):
    df = pd.DataFrame(generate_submissions_with_ticker(ticker, max_submissions, subno), columns=['User', 'Ticker', 'Text', "Timestamp", "Upvotes", "Ratio", "Subreddit"])
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    directory = os.path.join('..', 'Output_Data', 'With_Ticker', f'{ticker}')
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f'{ticker}_reddit_dataset_{timestamp}'
    filepath = os.path.join(directory, filename)
    df.to_csv(f'{filepath}.csv', index=False)
    print(f'{filename} exported to {filepath}')



#export_data_any_ticker(subno=-20)  #This works but it's glitching the progressbar ;)
export_data_any_ticker()