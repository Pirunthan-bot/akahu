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
    new_transactions = pd.json_normalize(data['items'])
    print("Data retrieved successfully!")

    # Load existing transactions if the file exists
    input_file_path = os.path.join(input_dir, 'transactions.json')
    if os.path.exists(input_file_path):
        with open(input_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
            existing_transactions = existing_data['transactions']
    else:
        existing_transactions = []

    # Convert transactions to DataFrame for easier comparison
    existing_df = pd.DataFrame(existing_transactions)
    new_df = pd.DataFrame(new_transactions)

    # Find new transactions by checking _id and date uniqueness
    if not existing_df.empty:
        combined_df = pd.concat([existing_df, new_df])
        updated_df = combined_df.drop_duplicates(subset=['_id', 'date'], keep='last')
    else:
        updated_df = new_df

    # Convert updated DataFrame back to dictionary format
    updated_data = {'transactions': updated_df.to_dict(orient='records')}

    # Save updated data to JSON file
    with open(input_file_path, 'w') as json_file:
        json.dump(updated_data, json_file, indent=4)

else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)  # Print the error message from the response
