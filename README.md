# About

Connects to Akahu and pulls transaction data and categorizes it using some basic python scripts. To run this you'll need to connect your banking app to akahu, which will be able to pull data from the banking apps and put it into an api for you to access.
You can call the api and get a list of transaction in the form of a json. I also had to write a couple scripts to categorise data where there was no categorisation available.

# How to

## Connecting to Akahu

First run the connect_to_akahu.py to connect to akahu and pull transaction data, but before you can do that you'll need to set up you akahu connection and store your api and user keys as windows environment variables:
* You can find more info on setting up connections in akahu here: https://developers.akahu.nz/docs/personal-apps
* The script calls windows environment variables that you'll need to set up. You can find out how to set up environment variables in windows here: https://gargankush.medium.com/storing-api-keys-as-environmental-variable-for-windows-linux-and-mac-and-accessing-it-through-974ba7c5109f

Once you've done that you'll see your transactions json in the inputs folder.

## Categorising data
Once you've got the transactions data as a json. you'll be able to run basic_categorisation_script.py
* This will categorise data in the first instance to get you some basic training data.
* you can update the catagories on line 36 - make sure that the keywords are in lowercase

Once you run this you'll get see some outputs in your outputs folder, the data is categorised somewhat. This process also generates the training data for the naive bayes model for categorising data. You can have a look at your others category and tag them appropriately in the training data.

## ML Categorisation
Once you've got the training data, you'll be able to run the ml_categorisation_script. This will load the training data you generated previously into a naive bayes model for machine learning then reapply to the description to give you ML based categorisation of transactions.
The success of the model will depend on how much training data you have.

This will generate some outputs labled "_ml"
