import configparser
import requests
import pandas as pd
from datetime import datetime, timedelta

# Read API access key from the configuration file
config = configparser.ConfigParser()
config.read('../config.txt')
access_key = config.get('Config', 'ACCESS_KEY')

# Define the date range for your requests
start_date = datetime(2018, 1, 1)
end_date = datetime(2023, 11, 12)
delta = timedelta(days=4)  

# Initialize an empty DataFrame to store the results
df = pd.DataFrame()

# Loop over the date range
current_date = start_date
while current_date <= end_date:
    # Format the current date as a string
    current_date_str = current_date.strftime('%Y-%m-%d')
    current_date_end = (current_date+delta).strftime('%Y-%m-%d')
    # Make the API request with the current date
    params = {
        'access_key': access_key,
        'date_from': current_date_str,
        'date_to': current_date_end,
    }

    api_result = requests.get('http://api.marketstack.com/v1/tickers/aapl/intraday', params)
    
    
    # Check if the request was successful (status code 200)
    if api_result.status_code == 200:
        api_response = api_result.json()
        # Check if 'intraday' data is present in the response
        if 'intraday' in api_response['data']:
            temp_df = pd.DataFrame(api_response['data']['intraday'])
            temp_df = temp_df.apply(pd.Series)
            df = pd.concat([df, temp_df])
    
    # Move to the next day
    current_date += delta

# Now df contains all the intraday data for the specified date range
df.to_csv('apple_all_data.csv')