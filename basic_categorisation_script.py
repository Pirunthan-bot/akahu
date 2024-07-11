import os
import json
import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Create the "data" directory if it doesn't exist
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Create the "data" directory if it doesn't exist
input_dir = 'input'
os.makedirs(input_dir, exist_ok=True)

# Load JSON data
input_file_path = os.path.join(input_dir, 'transactions.json')
with open(input_file_path) as json_file:
    data = json.load(json_file)


# Normalize JSON data into a DataFrame and rename headers
df = pd.json_normalize(data['transactions'])


#df.columns = ['transaction_id','account_id','user_id', 'connection_id','created_date_time','updated_date_time',"transaction_date","transaction_description",'amount','balance','payment_type', 'hash']

# Categorize transactions based on the description
descriptions = df['description']


# Example categories (you can expand this list)
categories = {
        'interest': ['interest', 'dividend'],
        'fees': ['fee', 'charge'],
        'payment': ['payment', 'paid'],
        'transfer': ['transfer'],
        'income': ['spendingspending', 'payroll']
        # Add more categories as needed
    }

    # Function to categorize based on keywords
def categorize(description):
        for category, keywords in categories.items():
            if any(keyword in description.lower() for keyword in keywords):
                return category
        return 'other'

# Apply categorization
df['category'] = df.apply(
        lambda row: row['category.name'] if pd.notnull(row['category.name']) else categorize(row['description']), 
        axis=1
    )

# Drop the old category.name column
df = df.drop(columns=['category.name'])

# Rename the new category column to category.name
df = df.rename(columns={'category': 'category.name'})

# Save the categorized data to a new JSON file
categorized_json_path = os.path.join(output_dir, 'categorized_transactions.json')
categorized_data = df.to_dict(orient='records')
with open(categorized_json_path, 'w') as json_file:
        json.dump(categorized_data, json_file, indent=4)

# Save to Excel
categorized_excel_path = os.path.join(output_dir, 'categorized_transactions.xlsx')
df.to_excel(categorized_excel_path, index=False)

print("Data saved to categorized_transactions.json and categorized_transactions.xlsx")
print(df[['date', 'description', 'category.name']])

training_data = df[['date', 'description', 'category.name']]

# Save to CSV
categorized_csv_path = os.path.join(input_dir, 'training_data.csv')
training_data.to_csv(categorized_csv_path , index=False)