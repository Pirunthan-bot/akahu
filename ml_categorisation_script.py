import os
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer


# Create the "data" directory if it doesn't exist
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Create the "data" directory if it doesn't exist
input_dir = 'input'
os.makedirs(input_dir, exist_ok=True)

# Convert to DataFrame
input_file_path = os.path.join(input_dir, 'training_data.csv')
train_df = pd.read_csv(input_file_path)

# Split data into descriptions and categories
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_df['description'])
y_train = train_df['category.name']

# Train Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)


# Load JSON data
input_file_path = os.path.join(input_dir, 'transactions.json')
with open(input_file_path) as json_file:
    data = json.load(json_file)
    
    # Normalize the transactions
    df_transactions = pd.json_normalize(data['items'])

    # Descriptions to be categorized
    descriptions = df_transactions['description']

    # Transform descriptions to vectors
    X_test = vectorizer.transform(descriptions)

    # Predict categories for descriptions
    predicted_categories = model.predict(X_test)
    df_transactions['category'] = predicted_categories

    # Save the categorized data to a new JSON file
    categorized_json_path = os.path.join(output_dir, 'categorized_transactions_ml.json')
    categorized_data = df_transactions.to_dict(orient='records')
    with open(categorized_json_path, 'w') as json_file:
        json.dump(categorized_data, json_file, indent=4)

    # Save to Excel
    categorized_excel_path = os.path.join(output_dir, 'categorized_transactions_ml.xlsx')
    df_transactions.to_excel(categorized_excel_path, index=False)

    df_summary = df_transactions[['date', 'description', 'category.name','category']]
    # Save to CSV
    categorized_csv_path = os.path.join(output_dir, 'summarized_transactions_ml.csv')
    df_summary.to_csv(categorized_csv_path, index=False)

    print("Data saved to categorized_transactions.json, categorized_transactions.xlsx, and categorized_transactions.csv")
    print(df_transactions[['date', 'description', 'category.name','category']])