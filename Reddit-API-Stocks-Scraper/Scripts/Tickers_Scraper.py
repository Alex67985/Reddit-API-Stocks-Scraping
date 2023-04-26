import pandas as pd
from yahoo_fin import stock_info as si
import os
from datetime import datetime

def export_tickers(df, exchange_index_name: str):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    directory = os.path.join('..', 'Input_Data', 'Tickers')
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f"{exchange_index_name.lower()}_tickers.csv"
    filepath = os.path.join(directory, filename)
    df.to_csv(filepath, index=False)
    return filename

def get_index_tickers(name: str): #Nasdaq and Other
    tickers = getattr(si, f"tickers_{name.lower()}")()
    tickers_df = pd.DataFrame(tickers, columns=['ticker'])
    export_tickers(df=tickers_df, exchange_index_name=name)

def get_sp500_tickers():
    sp500 = 'https://datahub.io/core/s-and-p-500-companies/r/constituents.csv'
    tickers_df = pd.read_csv(sp500).rename(columns={'Symbol': 'ticker'})
    tickers_df = tickers_df['ticker']
    export_tickers(df=tickers_df, exchange_index_name='S&P500')


get_index_tickers('Nasdaq')
get_index_tickers('Other')
get_sp500_tickers()

print('Tickers successfully exported')
