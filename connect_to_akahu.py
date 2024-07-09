import pandas as pd
import os
import requests
import json

# Create the "data" directory if it doesn't exist
input_dir = 'input'
os.makedirs(input_dir, exist_ok=True)

# Access environment variables
user_access_token = os.getenv('USER_TOKEN')
app_access_token = os.getenv('API_TOKEN')

# Check if the variables are loaded correctly
if not user_access_token or not app_access_token:
    raise ValueError("USER_ACCESS_TOKEN or APP_ACCESS_TOKEN not set in environment variables")

headers = {
    'Authorization': f'Bearer {user_access_token}',
    'X-Akahu-ID': app_access_token
}

# Make a request to the Akahu API
response = requests.get('https://api.akahu.io/v1/transactions', headers=headers)

# Handle the response
if response.status_code == 200:
    data = response.json()
    print("Data retrieved successfully!")
    # Process the data as needed


    # Save JSON response to a file
    input_file_path = os.path.join(input_dir, 'transactions.json')
    with open(input_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)  # Print the error message from the response
