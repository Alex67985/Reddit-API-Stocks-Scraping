import pandas as pd
from datetime import datetime
import os
import Reddit_Info as rd


def search_stocks_subreddits(
        member_count: int = 1,  #You can specify a minimum members count
        search_q: str = "investing OR trading OR finance OR stocks -gifs ", #You can specify a certain search pattern
        ticker: str = ' '  #You can search for a certain ticker
        ): 
    

    reddit = rd.reddit_info()
    
    subreddits = reddit.subreddits.search(
        search_q + ticker
    )
    data = []
    for subreddit in subreddits:
        data.append(
            {
                "Id": subreddit.id,
                "Subreddit": subreddit.display_name,
                "Members": subreddit.subscribers,
                "Description": subreddit.public_description,
            }
        )
    df = pd.DataFrame(data)
    df = df.sort_values(by="Members", ascending=False)
    df = df.dropna(subset=["Members"])
    df = df[df["Members"] >= member_count]
    df = df.reset_index(drop=True)
    return df




def export_subreddits(
        member_count: int = 1,  #You can specify a minimum members count
        search_q: str = "investing OR trading OR finance OR stocks -gifs ", #You can specify a certain search pattern
        ticker: str = ''  #You can search for a certain ticker
        ):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    df = search_stocks_subreddits(member_count, search_q, ticker)
    directory = os.path.join('..', 'Input_Data', 'Subreddits')
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f"{ticker}_subreddits_{timestamp}"
    filepath = os.path.join(directory, filename)
    df.to_csv(f'{filepath}.csv', index=False)
    return df

