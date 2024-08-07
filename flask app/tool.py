from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

def get_crypto_data(crypto_id):
    # Simulate data for the specified cryptocurrency
    data = {
        'price': np.random.rand(100),
        'market_cap': np.random.rand(100),
        '24hr_vol': np.random.rand(100),
        '24hr_change': np.random.rand(100),
        'last_updated_at': pd.date_range('1/1/2022', periods=100)
    }
    
    # Convert the simulated data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    return df

def analyze_trend(df, trend_name):
    if trend_name == 'daily_return':
        df['daily_return'] = df['price'].pct_change()
    elif trend_name == 'moving_average':
        df['moving_average'] = df['price'].rolling(window=7).mean()
    elif trend_name == 'exponential_moving_average':
        df['exponential_moving_average'] = df['price'].ewm(span=7, adjust=False).mean()
    
    return df

def combine_trends(df, trend1, trend2, trend3):
    df = analyze_trend(df, trend1)
    df = analyze_trend(df, trend2)
    df = analyze_trend(df, trend3)
    
    # Map trend names to actual column names
    trend_columns = {
        'daily_return': 'daily_return',
        'moving_average': 'moving_average',
        'exponential_moving_average': 'exponential_moving_average'
    }
    
    # Get the actual column names
    trend1_column = trend_columns.get(trend1)
    trend2_column = trend_columns.get(trend2)
    trend3_column = trend_columns.get(trend3)
    
    # Check if the trend columns exist
    if trend1_column and trend2_column and trend3_column:
        df['combined_trend'] = (df[trend1_column] + df[trend2_column] + df[trend3_column]) / 3
    else:
        print("Invalid trend names")
    
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        crypto_id = request.form['crypto_id']
        trend1 = request.form['trend1']
        trend2 = request.form['trend2']
        trend3 = request.form['trend3']
        
        df = get_crypto_data(crypto_id)
        df = combine_trends(df, trend1, trend2, trend3)
        
        return render_template('result.html', tables=[df.to_html()])
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)