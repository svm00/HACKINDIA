import pandas as pd
import web3
import time
from datetime import datetime

# Create a Web3 instance
w3 = web3.Web3(web3.providers.HTTPProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))

# Create a CoinGecko API instance
cg = CoinGeckoAPI()

def get_crypto_data(crypto_id):
    # Retrieve data for the specified cryptocurrency from CoinGecko
    data = cg.get_price(ids=crypto_id, vs_currencies='usd', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True)
    
    # Convert the retrieved data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Convert the 'last_updated_at' column to datetime format
    df['last_updated_at'] = pd.to_datetime(df['last_updated_at'], unit='s')
    
    return df

def analyze_trend(df, trend_name):
    # Analyze the trend (e.g., calculate daily returns, moving averages, etc.)
    if trend_name == 'daily_return':
        df['daily_return'] = df['price'].pct_change()
    elif trend_name == 'moving_average':
        df['moving_average'] = df['price'].rolling(window=7).mean()
    elif trend_name == 'exponential_moving_average':
        df['exponential_moving_average'] = df['price'].ewm(span=7, adjust=False).mean()
    
    return df

def combine_trends(df, trend1, trend2, trend3):
    # Combine the three trends together
    df = analyze_trend(df, trend1)
    df = analyze_trend(df, trend2)
    df = analyze_trend(df, trend3)
    
    # Create a new column that combines the three trends
    df['combined_trend'] = (df[trend1] + df[trend2] + df[trend3]) / 3
    
    return df

def main():
    # Ask the user for the type of cryptocurrency to search and predict
    crypto_id = input("Enter the cryptocurrency ID (e.g., bitcoin, ethereum, etc.): ")
    
    # Retrieve and analyze the data
    df = get_crypto_data(crypto_id)
    
    # Ask the user for the three trends to combine
    trend1 = input("Enter the first trend (e.g., daily_return, moving_average, etc.): ")
    trend2 = input("Enter the second trend (e.g., daily_return, moving_average, etc.): ")
    trend3 = input("Enter the third trend (e.g., daily_return, moving_average, etc.): ")
    
    # Combine the three trends together
    df = combine_trends(df, trend1, trend2, trend3)
    
    # Print the results
    print(df)

if __name__ == "__main__":
    main()